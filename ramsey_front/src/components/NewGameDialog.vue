<template>
  <v-dialog v-model="show" max-width="450">
    <v-container >
      <v-form v-model="valid">
        <v-text-field
          v-model="name"
          :counter="10"
          :rules="nameRules"
          label="Name"
          required
        ></v-text-field>
        <v-text-field
          v-model="gameSize"
          label="Game Size"
          :rules="gameSizeRules"
          required
        ></v-text-field>
        <v-text-field
          v-model="cliqueSize"
          label="Winning clique Size"
          :rules="cliqueSizeRules"
          required
        ></v-text-field>
        <v-btn
          :disabled="!valid"
          @click="submit"
        >
          submit
        </v-btn>
        <v-btn color="error" @click.stop="show=false">close</v-btn>
      </v-form>
    </v-container>
  </v-dialog>
</template>

<script>
    import axios from 'axios'
    export default {
        name: "NewGameDialog",
        props: ['visible'],
        computed: {
          show: {
            get() {
              return this.visible
            },
            set(value) {
              if (!value) {
                this.$emit('close')
              }
            }
          }
        },
        data() {
          return {
            valid: false,
            nameRules: [
              v => !!v || 'Name is required',
              v => v.length <= 10 || 'Name must be less than 10 characters'
            ],
            name: '',
            gameSize: '7',
            gameSizeRules: [
              v => !!v || 'Game size is required',
              v => /^\d+$/.test(v) || 'Expected number',
              v => v <= 100 || 'Game size must be less than 100',
            ],
            cliqueSize: '3',
            cliqueSizeRules: [
              v => !!v || 'Game size is required',
              v => /^\d+$/.test(v) || 'Expected number',
              v => v <= 100 || 'Game size must be less than 100',
            ],
          }
        },
        methods: {
          submit() {
            var data = {
              data: {
                game_name: this.name,
                graph_size: this.gameSize,
                clique_size: this.cliqueSize,
              }
            };
            axios
              .post(
                'http://0.0.0.0:8000/games', data,
                {headers: {'Access-Control-Allow-Origin': '*',}}
              )
              .then(
                this.$emit('submitted')
              )
          }
        }
    }
</script>

<style scoped>

</style>
