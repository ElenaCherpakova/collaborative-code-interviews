import '@testing-library/jest-dom';

// Mock scrollIntoView
window.HTMLElement.prototype.scrollIntoView = function() {};

// Mock pointer capture methods required by Radix UI
window.HTMLElement.prototype.hasPointerCapture = function() { return false; };
window.HTMLElement.prototype.setPointerCapture = function() {};
window.HTMLElement.prototype.releasePointerCapture = function() {};

// Mock performance.now
if (!global.performance) {
  global.performance = {
    now: () => Date.now(),
    timeOrigin: Date.now(),
    toJSON: () => ({}),
    clearMarks: () => {},
    clearMeasures: () => {},
    clearResourceTimings: () => {},
    getEntries: () => [],
    getEntriesByName: () => [],
    getEntriesByType: () => [],
    mark: () => ({}),
    measure: () => ({}),
    setResourceTimingBufferSize: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
    dispatchEvent: () => false,
  } as unknown as Performance;
}
