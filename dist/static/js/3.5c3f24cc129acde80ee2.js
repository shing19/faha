webpackJsonp([3],{"CaE/":function(n,t,e){"use strict";var a=function(){var n=this,t=n.$createElement,e=n._self._c||t;return e("div",[e("p",[n._v("Home page")]),n._v(" "),e("p",[n._v("Random number from backend: "+n._s(n.randomNumber))]),n._v(" "),e("button",{on:{click:n.getRandom}},[n._v("New random number")]),n._v(" "),e("p",[n._v("Nice to meet you")])])},o=[],r={render:a,staticRenderFns:o};t.a=r},Fs8J:function(n,t,e){"use strict";var a=e("mtWM"),o=e.n(a);t.a={data:function(){return{randomNumber:0}},methods:{getRandomInt:function(n,t){return n=Math.ceil(n),t=Math.floor(t),Math.floor(Math.random()*(t-n+1))+n},getRandom:function(){this.randomNumber=this.getRandomFromBackend()},getRandomFromBackend:function(){var n=this;o.a.get("http://localhost:5000/api/random").then(function(t){n.randomNumber=t.data.randomNumber}).catch(function(n){console.log(n)})}},created:function(){this.getRandom()}}},lO7g:function(n,t,e){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=e("Fs8J"),o=e("CaE/"),r=e("VU/8"),u=r(a.a,o.a,!1,null,null,null);t.default=u.exports}});
//# sourceMappingURL=3.5c3f24cc129acde80ee2.js.map