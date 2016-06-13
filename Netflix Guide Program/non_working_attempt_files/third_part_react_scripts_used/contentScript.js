/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	/**
	 * Copyright (c) 2015-present, Facebook, Inc.
	 * All rights reserved.
	 *
	 * This source code is licensed under the BSD-style license found in the
	 * LICENSE file in the root directory of this source tree. An additional grant
	 * of patent rights can be found in the PATENTS file in the same directory.
	 *
	 * 
	 */
	'use strict';

	/* global self */

	if (Object.keys(unsafeWindow.__REACT_DEVTOOLS_GLOBAL_HOOK__._renderers).length) {
	  self.port.emit('hasReact', true);
	  injectBackend();
	} else {
	  self.port.emit('hasReact', false);
	}

	window.addEventListener('beforeunload', function () {
	  self.port.emit('unload');
	});

	function connectToBackend() {
	  self.port.on('message', function (payload) {
	    window.postMessage({
	      source: 'react-devtools-reporter',
	      payload: payload
	    }, '*');
	  });

	  window.addEventListener('message', function (evt) {
	    if (!evt.data || evt.data.source !== 'react-devtools-bridge') {
	      return;
	    }

	    self.port.emit('message', evt.data.payload);
	  });
	}

	function injectBackend() {
	  var node = document.createElement('script');

	  node.onload = function () {
	    window.postMessage({ source: 'react-devtools-reporter' }, '*');

	    connectToBackend();
	    node.parentNode.removeChild(node);
	  };

	  node.src = 'resource://react-devtools/data/build/backend.js';
	  document.documentElement.appendChild(node);
	}

/***/ }
/******/ ]);