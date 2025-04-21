export function onMounted(callback) {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", callback);
  } else {
    // Document already loaded
    callback();
  }
}

export function setup(data, appName = 'app') {
  document.addEventListener('alpine:init', () => {
    window.Alpine.data(appName, () => data)
  })
}
