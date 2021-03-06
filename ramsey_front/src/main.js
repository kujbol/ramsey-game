// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import Vuetify from 'vuetify'

import App from './App'
import NewGameDialog from './components/NewGameDialog'
import GameList from './components/GameList'

import 'vuetify/dist/vuetify.min.css'

const serverUrl = process.env['SERVER_URL'];
const webSocketServerUrl = process.env['WS_SERVER_URL'];

Vue.use(Vuetify, { theme: {
  primary: '#ee44aa',
  secondary: '#424242',
  accent: '#82B1FF',
  error: '#FF5252',
  info: '#2196F3',
  success: '#4CAF50',
  warning: '#FFC107'
}});

Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App, NewGameDialog, GameList},
  template: '<App/>'
});


export {serverUrl, webSocketServerUrl}
