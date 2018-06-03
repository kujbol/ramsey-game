import Vue from 'vue'
import Router from 'vue-router'
import Game from '@/components/Game'
import GameList from '@/components/GameList'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/game/:roomId',
      name: 'game',
      component: Game
    },
    {
      path: '/',
      name: 'game_list',
      component: GameList
    }
  ]
})
