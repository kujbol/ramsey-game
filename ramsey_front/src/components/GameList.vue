<template>
  <v-container fluid>
    <v-data-table
      :headers="headers"
      :items="games"
      hide-actions
      class="elevation-5"
    >
      <template slot="items" slot-scope="props">
        <td>{{props.item.id}}</td>
        <td>{{props.item.name}}</td>
        <td >{{ props.item.state }}</td>
        <td>{{ props.item.size }}</td>
        <td>{{ props.item.finish_size }}</td>
        <td>{{ props.item.player_count }}</td>
        <td>
          <v-btn icon class="mx-0" :to="{name: 'game', params: { roomId: props.item.id }}">
            <v-icon color="primary">mouse</v-icon>
          </v-btn>
        </td>
      </template>
    </v-data-table>
    <v-btn color="primary" @click.stop="newGameDialog = true">Create Game</v-btn>
    <new-game-dialog :visible="newGameDialog" @close="newGameDialog=false" @submitted="submitted()"></new-game-dialog>
  </v-container>
</template>

<script>
    import axios from 'axios'
    import NewGameDialog from './NewGameDialog'

    export default {
      name: "GameList",
      components: {
        'new-game-dialog': NewGameDialog,
      },
      data(){
        return{
          newGameDialog: false,
          games: [],
          headers: [
            {text: 'Id', value: 'id'},
            {text: 'Name', value: 'name'},
            {text: 'State', value: 'state'},
            {text: 'Graph size', value: 'size'},
            {text: 'Clique size', value: 'finish_size'},
            {text: 'Players', value: 'player_count'},
            {text: 'Join game', value: 'join_game', sortable: false}
          ],
        }
      },
      mounted(){
        this.loadList();
      },
      methods: {
        loadList: function () {
          axios
            .get(
              'http://0.0.0.0:8000/games',
              {headers: {'Access-Control-Allow-Origin': '*',}}
            )
            .then(response => {
              this.games = response.data.data.games;
              setTimeout(this.loadList, 2000)
            })
        },
        submitted: function () {
          this.newGameDialog=false;
          axios
            .get(
              'http://0.0.0.0:8000/games',
              {headers: {'Access-Control-Allow-Origin': '*',}}
            )
            .then(response => {
              this.games = response.data.data.games;
            })
        }
      }
    }
</script>

<style scoped>

</style>
