/* KaTeX 0.18.7; explicit delimiters only. Original records remain literal. */
(() => {
  const options = {
    delimiters: [
      {left: '\\[', right: '\\]', display: true},
      {left: '\\(', right: '\\)', display: false},
    ],
    ignoredClasses: ['verbatim', 'original-message', 'original-source', 'no-math', 'katex'],
    throwOnError: false,
    trust: false,
    output: 'htmlAndMathml',
  };
  const observer = new MutationObserver(() => {
    if (pending) return;
    pending = requestAnimationFrame(render);
  });
  let pending = 0;
  function render() {
    pending = 0;
    observer.disconnect();
    renderMathInElement(document.body, options);
    observer.observe(document.body, {childList: true, characterData: true, subtree: true});
  }
  render();
})();
