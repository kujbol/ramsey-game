<template>
  <v-container id="main-container">
    <v-alert v-for="alert in alerts" :color=alert.type :icon=alert.type :key=alert.id v-model=alert.open transition="scale-transition" dismissible>
      {{ alert.details }}
    </v-alert>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <svg width=1500 height="650">
          <g class="links"></g>
          <g class="nodes"></g>
        </svg>
      </v-layout>
    </v-slide-y-transition>
    <v-dialog v-model="dialog" persistent max-width="380">
      <v-card>
        <v-card-title class="headline">Waiting for other players to join</v-card-title>
        <v-card-text>
          <v-layout align-center justify-center>
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </v-layout>
        </v-card-text>
      </v-card>
    </v-dialog>


  </v-container>
</template>

<script>
  import Vue from 'vue'
  import * as d3 from 'd3'
  import * as d3color from 'd3-scale-chromatic'

  export default Vue.extend({
    data () {
      return {
        ws: null,
        graphData: {
          nodes: [],
          links: [],
        },
        dialog: true,
        alerts: [],
      }
    },
    methods:{
      renderGraph() {
        var color = d3color.schemeCategory10;
        var svg = d3.select("svg"),
          width = 1500,
          height = 650;

        var simulation = d3.forceSimulation(this.graphData.nodes)
          .force('charge', d3.forceManyBody().strength(-10000))
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('link', d3.forceLink().links(this.graphData.links))
          .on('tick', ticked);


        d3.select('.links')
          .selectAll('line')
          .data(this.graphData.links);

        var graphData = this.graphData;
        var ws = this.ws;
        var colorMapping = {0: color[5]};

        function colorFromUUID(uuid) {
          var mappedColor = colorMapping[uuid];
          if (mappedColor === undefined){
            mappedColor = color[Object.keys(colorMapping).length + 1];
            colorMapping[uuid] = mappedColor;
          }
          return mappedColor;
        }

        function updateLinks() {
          var u = d3.select('.links')
            .selectAll('line')
            .data(graphData.links)
            .on("click", function(event){
              var move_request = {
                type: 'MSG_MOVE',
                start_node: event.source.index,
                end_node: event.target.index
              };
              ws.send(JSON.stringify(move_request));
              console.log(move_request);
            });

          u.enter()
            .append('line')
            .merge(u)
            .attr('x1', function(d) {
              return d.source.x
            })
            .attr('y1', function(d) {
              return d.source.y
            })
            .attr('x2', function(d) {
              return d.target.x
            })
            .attr('y2', function(d) {
              return d.target.y
            })
            .attr("stroke-width", 10 )
            .attr("stroke", function(d) { return colorFromUUID(d.player); });

          u.exit().remove()
        }

        function updateNodes() {
          var u = d3.select('.nodes')
            .selectAll('text')
            .data(graphData.nodes)
              .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

          u.enter()
            .append('text')
            .text(function(d) {
              return d.id
            })
            .merge(u)
            .attr('x', function(d) {
              return d.x
            })
            .attr('y', function(d) {
              return d.y
            })
            .attr('dy', function(d) {
              return 10;
            });

          u.exit().remove()
        }

        function ticked() {
          updateLinks();
          updateNodes();
        }

        function dragstarted(d) {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }

        function dragged(d) {
          d.fx = d3.event.x;
          d.fy = d3.event.y;
        }

        function dragended(d) {
          if (!d3.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }
      }
    },
    mounted () {
      this.renderGraph()
    },
    watch: {
      graphData: {
        handler: 'renderGraph',
        deep: true
      }
    },
    created: function() {
      var gameComponent = this;
      var messageCounter = 0;
      this.ws = new WebSocket(
        'ws://0.0.0.0:8000/game/' + this.$route.params.roomId
      );
      var ws = this.ws;
      this.ws.addEventListener('open', function (e) {
        ws.send(JSON.stringify({'type': 'MSG_CONNECT'}))
      });
      this.ws.addEventListener('message', function (e) {
        var msg = JSON.parse(e.data);
        console.log(msg);
        if (msg.type === "MSG_GAME") {
          gameComponent.$data.dialog = false;

          var graphData = msg.body.available_graph;
          for (let link of graphData.links) {
            link.player = 0;
          }

          for (const [player, player_graph] of Object.entries(msg.body.players_graph)) {
            for (var i = 0; i < player_graph.links.length; i++){
              player_graph.links[i].player = player;
            }
            graphData.links.push(...player_graph.links);
            console.log(graphData.links.length)
          }
          gameComponent.graphData = graphData;
        }

        if (msg.type === "MSG_MOVE") {
        }

        if (msg.type === "MSG_INFO") {
          messageCounter = messageCounter + 1;
          gameComponent.$data.alerts.push(
            {type: 'info', details: msg.body.details, id: messageCounter, open: true}
            )
        }
        if (msg.type === "MSG_ERROR") {
          messageCounter = messageCounter + 1;
          gameComponent.$data.alerts.push(
            {type: 'error', details: msg.body.details, id: messageCounter, open: true}
          )
        }
        if (msg.type === "MSG_WON") {
        messageCounter = messageCounter + 1;
        gameComponent.$data.alerts.push(
            {type: 'success', details: msg.body.details, id: messageCounter, open: true}
          )
        }
      });
    }
  })
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .nodes {
      fill: cadetblue;
    }
    .links {
      stroke: #FFFFFF;
      stroke-opacity: 0.6;
    }
</style>
