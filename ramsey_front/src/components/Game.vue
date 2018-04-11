<template>
  <v-container>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center>
        <svg width=800 height="600">
          <g class="links"></g>
          <g class="nodes"></g>
        </svg>
      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
  import Vue from 'vue'
  import * as d3 from 'd3'

  export default Vue.extend({
    data () {
      return {
        ws: null,
        graphData: {
          nodes: [],
          links: [],
        },
      }
    },
    methods:{
      renderGraph() {
        var svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height");

        var simulation = d3.forceSimulation(this.graphData.nodes)
          .force('charge', d3.forceManyBody().strength(-6000))
          .force('center', d3.forceCenter(width / 2, height / 2))
          .force('link', d3.forceLink().links(this.graphData.links))
          .on('tick', ticked);

        var graphData = this.graphData;
        function updateLinks() {
          var u = d3.select('.links')
            .selectAll('line')
            .data(graphData.links);

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
            .attr("stroke-width", function(d) { return Math.sqrt(5); });

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
            })

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
          gameComponent.graphData = msg.body.available_graph;

        };
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
