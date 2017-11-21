import 'select2';
import queryString from 'query-string';

let supportsPassive = false;
try {
  let opts = Object.defineProperty({}, 'passive', {
    get: function () {
      supportsPassive = true;
    }
  });
  window.addEventListener('test', null, opts);
} catch (e) {
}

export function onScroll(func) {
  window.addEventListener('scroll', func, supportsPassive ? {passive: true} : false);
}

export function initSelects() {
  $('select:not(.browser-default):not([multiple])').material_select();
  $('select[multiple]:not(.browser-default)').select2({width: '100%'});
}

export function removeFromQuery(name, value) {
  const urlParams = queryString.parse(location.search);
  if (Array.isArray(urlParams[name])) {
    delete urlParams[name][urlParams[name].indexOf(value)];
  } else {
    delete urlParams[name];
  }
  return queryString.stringify(urlParams);
}
