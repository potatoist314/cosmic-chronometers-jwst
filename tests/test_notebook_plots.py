"""The fit notebook skips only figures when CERIDWEN_PLOTS=0.

The GPU runner sets CERIDWEN_PLOTS=0 because figures render nothing under the
Agg backend; scripts/regenerate_fit_notebooks.py rebuilds them locally. These
tests prove, without executing the notebook, that with plots off every name
loaded outside an `if PLOTS:` gate is still defined, every plt.show sits
inside a gate, and the runner/preflight contracts still hold.
"""
import ast
import builtins
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks/ceridwen_integrated_photometry_spectra.ipynb"

# IPython injects display() into the notebook namespace; it is never imported.
ALLOWED = set(dir(builtins)) | {"display"}


def code_cells():
    notebook = json.loads(NOTEBOOK.read_text())
    return [(index, "".join(cell["source"])) for index, cell in enumerate(notebook["cells"])
            if cell["cell_type"] == "code"]


def is_plots_gate(node):
    return (isinstance(node, ast.If) and isinstance(node.test, ast.Name)
            and node.test.id == "PLOTS" and not node.orelse)


def bound_names(target):
    """Names bound by an assignment/for/with/except target."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        return set().union(*(bound_names(e) for e in target.elts))
    if isinstance(target, ast.Starred):
        return bound_names(target.value)
    return set()


class Flow(ast.NodeVisitor):
    """Collect defs and uses, split by inside/outside `if PLOTS:` gates.

    Function bodies are deferred: their free variables must exist by the end
    of the notebook, since calls happen after all cells run.
    """

    def __init__(self):
        self.gated = False
        self.ext_defs, self.ext_uses = set(), set()
        self.gated_defs, self.gated_uses = set(), set()
        self.deferred = set()
        self.shows_outside = 0
        self.deferred_shows = 0

    def _defs(self):
        return self.gated_defs if self.gated else self.ext_defs

    def _uses(self):
        return self.gated_uses if self.gated else self.ext_uses

    def use(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                self._uses().add(child.id)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self._uses().add(node.id)
        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            if isinstance(node.ctx, ast.Del):
                self._uses().add(node.id)
            else:
                self._defs().add(node.id)

    def visit_AugAssign(self, node):
        self.visit(node.value)
        for child in ast.walk(node.target):
            if isinstance(child, ast.Name):
                self._uses().add(child.id)
        self._defs().update(bound_names(node.target))

    def visit_If(self, node):
        if is_plots_gate(node):
            self.use(node.test)
            outer = self.gated
            self.gated = True
            for statement in node.body:
                self.visit(statement)
            self.gated = outer
        else:
            self.generic_visit(node)

    def _function(self, node, bound):
        for default in list(node.args.defaults) + [d for d in node.args.kw_defaults if d]:
            self.use(default)
        for decorator in node.decorator_list:
            self.use(decorator)
        self._defs().add(bound)
        inner = Flow()
        inner.gated = self.gated
        for statement in node.body:
            inner.visit(statement)
        local = {a.arg for a in node.args.args}
        local |= {a.arg for a in node.args.posonlyargs + node.args.kwonlyargs}
        if node.args.vararg:
            local.add(node.args.vararg.arg)
        if node.args.kwarg:
            local.add(node.args.kwarg.arg)
        self.deferred |= ((inner.ext_uses | inner.gated_uses | inner.deferred)
                          - inner.ext_defs - inner.gated_defs - local)
        self.gated_defs |= inner.gated_defs - local if self.gated else set()
        if not self.gated:
            self.ext_defs |= inner.ext_defs - local
        self.deferred_shows += inner.shows_outside  # shows in bodies render at call time

    def visit_FunctionDef(self, node):
        self._function(node, node.name)

    def visit_AsyncFunctionDef(self, node):
        self._function(node, node.name)

    def visit_Lambda(self, node):
        bound = {a.arg for a in node.args.args}
        inner = Flow()
        inner.gated = self.gated
        inner.visit(node.body)
        self.deferred |= (inner.ext_uses | inner.gated_uses) - inner.ext_defs - bound

    def _comprehension(self, node):
        bound = set().union(*(bound_names(g.target) for g in node.generators))
        # Only the first iterable is eager; the rest runs with the targets bound.
        self.use(node.generators[0].iter)
        inner = Flow()
        inner.gated = self.gated
        for generator in node.generators[1:]:
            inner.visit(generator.iter)
            for condition in generator.ifs:
                inner.visit(condition)
        for condition in node.generators[0].ifs:
            inner.visit(condition)
        for child in (getattr(node, "elt", None), getattr(node, "key", None),
                      getattr(node, "value", None)):
            if child is not None:
                inner.visit(child)
        uses = (inner.ext_uses | inner.gated_uses) - bound - inner.ext_defs - inner.gated_defs
        self._uses().update(uses)

    def visit_ListComp(self, node):
        self._comprehension(node)

    def visit_SetComp(self, node):
        self._comprehension(node)

    def visit_DictComp(self, node):
        self._comprehension(node)

    def visit_GeneratorExp(self, node):
        self._comprehension(node)

    def visit_Import(self, node):
        self._defs().update({(a.asname or a.name).split(".")[0] for a in node.names})

    def visit_ImportFrom(self, node):
        self._defs().update({a.asname or a.name for a in node.names if a.name != "*"})

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "show" and not self.gated:
            self.shows_outside += 1
        self.generic_visit(node)


def analyze(source):
    flow = Flow()
    flow.visit(ast.parse(source))
    return flow


def test_plots_flag_defaults_on():
    cell2 = dict(code_cells())[2]
    assert 'PLOTS = os.environ.get("CERIDWEN_PLOTS", "1") == "1"' in cell2


def test_every_cell_compiles():
    for index, source in code_cells():
        compile(source, f"cell{index}", "exec")


def test_every_show_call_is_gated():
    for index, source in code_cells():
        flow = analyze(source)
        assert flow.shows_outside == 0, f"cell {index} shows a figure with PLOTS=0"
        assert flow.deferred_shows == 0, f"cell {index} hides a show call in a function"


def test_gated_names_are_never_needed_with_plots_off():
    """With PLOTS=0, every loaded name is defined outside a gate or deferred."""
    defined, deferred, flows = set(), set(), {}
    for index, source in code_cells():
        flow = analyze(source)
        flows[index] = flow
        missing = flow.ext_uses - defined - flow.ext_defs - ALLOWED
        assert not missing, f"cell {index} loads {sorted(missing)} with PLOTS=0"
        defined |= flow.ext_defs
        deferred |= flow.deferred
    assert not deferred - defined - ALLOWED, f"deferred loads: {sorted(deferred - defined - ALLOWED)}"
    gated_only = set().union(*(f.gated_defs for f in flows.values())) - defined - ALLOWED
    assert gated_only, "expected figure-only names behind the gates"
    for index, flow in flows.items():
        assert not flow.ext_uses & gated_only, f"cell {index} needs a gated name with PLOTS=0"


def test_runner_and_preflight_contracts_hold():
    import sys
    sys.path.insert(0, str(ROOT))
    from scripts import benchmark as engine
    assert "CERIDWEN_PLOTS='0'" in (ROOT / "scripts/experiment.py").read_text()
    top = dict(code_cells())[2]
    assert engine.literal(top, "SETTINGS")["sampler"]["num_live"] > 0
    node = next(n.value for n in ast.parse(top).body if isinstance(n, ast.Assign)
                and any(getattr(t, "id", None) == "PRIORS" for t in n.targets))
    assert {ast.literal_eval(k) for k in node.keys} >= {"logmass", "Z", "afe"}
    assert "joint_result = run_sampler(" in dict(code_cells())[10]
