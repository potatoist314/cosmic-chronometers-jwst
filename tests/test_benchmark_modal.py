"""Check the Modal benchmark summary arithmetic without Modal calls or a GPU."""
import json

import pytest

from scripts import benchmark_modal as bench
from scripts import modal_gpu


def test_h100_without_upgrade_bills_as_h100_and_b300_has_its_published_price():
    assert bench.rate_usd_per_second('H100!') == bench.rate_usd_per_second('H100')
    # https://modal.com/pricing: B300 $0.001972/s.
    assert bench.rate_usd_per_second('B300') == pytest.approx(
        0.001972 + modal_gpu.CPU_CORES * 0.0000131 + modal_gpu.MEMORY_GIB * 0.00000222)


def write_run(root, gpu, sampling):
    """One run directory: a container per entry of `sampling`, each holding those fit times."""
    cell = {'arm': 'fit', 'target': 'M1_210210', 'target_metadata': {'object_id': 210210}}
    containers = {}
    for index, times in enumerate(sampling):
        name = f'{index}-fc-{index}'
        directory = root / 'containers' / name
        (directory / 'results').mkdir(parents=True)
        stages = {'bootstrap': {'started': 10, 'finished': 20, 'exit': 0},
                  'throughput': {'started': 20, 'finished': 25, 'exit': 0}}
        stages.update({f'fit-{k}': {'started': 25, 'finished': 25 + t + 30, 'exit': 0, 'seconds': t}
                       for k, t in enumerate(times)})
        (directory / 'status.json').write_text(json.dumps({
            'gpu': gpu, 'stages': stages,
            'marks': {'entered': 2, 'unpacked': 3, 'grid_read': 5, 'finished': 200}}))
        (directory / 'results/throughput.json').write_text(json.dumps({'summary': [{'free_us_per_call': 20.0}]}))
        containers[name] = {'call_id': f'fc-{index}', 'spawned': 0, 'packed': 201, 'received': 203}
    (root / 'manifest.json').write_text(json.dumps({
        'gpus': [gpu], 'source': {'commit': 'abc', 'experiment': [cell]},
        'attempts': [{'containers': containers, 'billed_usd': 0.5}]}))
    return root


def test_relative_speed_and_cost_use_the_reference_median(tmp_path, monkeypatch):
    def fit_record(directory, stage):
        seconds = stage['seconds']
        return {'sampling_s': seconds, 'sampling_calls_per_s': 1e6 / seconds, 'compile_s': 5,
                'model_and_grid_cell_s': 2, 'post_fit_cells_s': 3, 'fit_stage_s': seconds + 30,
                'log_evidence': 1.0, 'log_evidence_err': 0.2,
                'posterior': {'logmass': {'q16': 0.9, 'q50': 1.0, 'q84': 1.1}}}

    monkeypatch.setattr(bench, 'fit_record', fit_record)
    reference = write_run(tmp_path / 'l40s', 'L40S', [[100, 100], [110, 110], [90, 90]])
    fast = write_run(tmp_path / 'h100', 'H100!', [[50, 50], [55, 55], [45, 45]])
    output = tmp_path / 'summary.json'
    bench.summarize(bench.parser().parse_args(
        ['summarize', str(reference), str(fast), '--reference', 'L40S', '--output', str(output)]))
    cards = json.loads(output.read_text())['cards']
    h100 = cards['H100!']
    assert cards['L40S']['relative_sampling_speed']['median'] == 1
    assert h100['relative_sampling_speed']['median'] == pytest.approx(2)
    assert (h100['relative_sampling_speed']['min'], h100['relative_sampling_speed']['max']) == pytest.approx(
        (100 / 55, 100 / 45))
    assert h100['relative_sampling_cost'] == pytest.approx(
        bench.rate_usd_per_second('H100!') * 50 / (bench.rate_usd_per_second('L40S') * 100))
    assert h100['container_start_s']['median'] == 2
    assert h100['retrieval_s']['median'] == 2
    assert h100['throughput_calls_per_s']['median'] == pytest.approx(5e4)
    # Setup 1 + grid 2 + bootstrap 10 + first fit stage + packing 1.
    assert h100['container_usd_per_fit'] == pytest.approx(bench.rate_usd_per_second('H100!') * (14 + 50 + 30))
