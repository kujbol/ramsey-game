<!--<template>-->
  <!--<v-container fluid>-->
    <!--<v-slide-y-transition mode="out-in">-->
      <!--<v-layout column align-center>-->
        <!--<img src="@/assets/logo.png" alt="Vuetify.js" class="mb-5">-->
        <!--<blockquote>-->
          <!--&#8220;First, solve the problem. Then, write the code.&#8221;-->
          <!--<footer>-->
            <!--<small>-->
              <!--<em>&mdash;John Johnson</em>-->
            <!--</small>-->
          <!--</footer>-->
        <!--</blockquote>-->
      <!--</v-layout>-->
    <!--</v-slide-y-transition>-->
  <!--</v-container>-->
<!--</template>-->

<template>
  <v-container>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <cytoscape :config="config" style="width: 100%; height: 650px"/>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
  const config =  {
    elements: [
      { // node a
        data: { id: 'a' }
      }, { // node b
        data: { id: 'b' }
      }, { // edge ab
        data: { id: 'ab', source: 'a', target: 'b' }
      }
    ],
    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#666',
          // 'label': 'data(id)'
        }
      },
      {
        selector: 'edge',
        style: {
          'width': 3,
          'line-color': '#ccc',
          'target-arrow-color': '#ccc',
          'target-arrow-shape': 'triangle'
        }
      }
    ],
    layout: {
      name: 'grid',
      rows: 1
    }
  };

  export default {
    data () {
      return {
        config: config,
      }
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
