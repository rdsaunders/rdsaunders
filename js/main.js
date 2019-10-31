// Remove the no JS class so that the button will show
document.documentElement.classList.remove('no-js');

const STORAGE_KEY = 'user-color-scheme';
const COLOR_MODE_KEY = '--color-mode';

const modeToggleButton = document.querySelector('.js-mode-toggle');
const modeStatusElement = document.querySelector('.js-mode-status');

/**
 * Pass in a custom prop key and this function will return its
 * computed value. 
 * A reduced version of this: https://andy-bell.design/wrote/get-css-custom-property-value-with-javascript/
 */
const getCSSCustomProp = (propKey) => {
  let response = getComputedStyle(document.documentElement).getPropertyValue(propKey);

  // Tidy up the string if there’s something to work with
  if (response.length) {
    response = response.replace(/\'|"/g, '').trim();
  }

  // Return the string response by default
  return response;
};

/**
 * Takes either a passed settings ('light'|'dark') or grabs that from localStorage.
 * If it can’t find the setting in either, it tries to load the CSS color mode,
 * controlled by the media query
 */
const applySetting = passedSetting => {
  let currentSetting = passedSetting || localStorage.getItem(STORAGE_KEY);
  
  if(currentSetting) {
    document.documentElement.setAttribute('data-user-color-scheme', currentSetting);
    setButtonLabelAndStatus(currentSetting);
  }
  else {
    setButtonLabelAndStatus(getCSSCustomProp(COLOR_MODE_KEY));
  }
}

/**
 * Get’s the current setting > reverses it > stores it
 */
const toggleSetting = () => {
  let currentSetting = localStorage.getItem(STORAGE_KEY);
  
  switch(currentSetting) {
    case null:
      currentSetting = getCSSCustomProp(COLOR_MODE_KEY) === 'dark' ? 'light' : 'dark';
      break;
    case 'light':
      currentSetting = 'dark';
      break;
    case 'dark':
      currentSetting = 'light';
      break;
  }

  localStorage.setItem(STORAGE_KEY, currentSetting);
  
  return currentSetting;
}

/**
 * A shared method for setting the button text label and visually hidden status element 
 */
const setButtonLabelAndStatus = currentSetting => { 
  modeToggleButton.setAttribute('aria-label', `Enable ${currentSetting === 'dark' ? 'light' : 'dark'} mode`);
  modeToggleButton.innerText = `${currentSetting === 'dark' ? '☀' : '☾'}`;
  modeStatusElement.innerText = `Color mode is now "${currentSetting}"`;
}

/**
 * Clicking the button runs the apply setting method which grabs its parameter
 * from the toggle setting method.
 */
modeToggleButton.addEventListener('click', evt => {
  evt.preventDefault();
  
  applySetting(toggleSetting());
});

applySetting();

// Progressively enhance links to embedded content
//
// Requires an element with the following markup:
// <div data-embed-src="[embed iframe url]" data-embed-type="[embed type]">
//   <p><a class="button" href="[embed url]">[Fallback button text]</a></p>
// </div>

(function (win, doc) {
    'use strict';
  
    var div = doc.getElementsByTagName('div'); // Embed.rb generates a <div> element, so look for those first
  
    for (var i = 0; i < div.length; i = i + 1) {
  
      // If a <div> has the right attributes…
      if (div[i].hasAttribute('data-embed-src')) {
        var embed = div[i];
        var type = embed.getAttribute('data-embed-type');
        var src = embed.getAttribute('data-embed-src');
        var title = embed.getAttribute('data-embed-title');
  
        embed.className += ' embed--' + type;
        embed.innerHTML = '<iframe class="embed-iframe" src="' + src + '" width="500" height="300" frameborder="0" title="' + title + '" allowfullscreen></iframe>';
        embed.removeAttribute('data-embed-src');
        embed.removeAttribute('data-embed-type');
        embed.removeAttribute('data-embed-title');
      }
    }
  
  }(this, this.document));