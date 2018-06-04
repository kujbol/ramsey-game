<template>
  <v-container fluid fill-height>

    <v-layout justify-center align-center fill-height>
      <v-flex d-flex>
        <v-container id="main-container">
          <v-alert v-for="alert in alerts" :color=alert.type :icon=alert.type :key=alert.id v-model=alert.open transition="scale-transition" dismissible>
            {{ alert.details }}
          </v-alert>
          <v-slide-y-transition mode="out-in">
            <v-layout column align-center>
              <svg id="svg-graph" width=1500 height="630">
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
      </v-flex>
    </v-layout>
    <!--<v-speed-dial fixed right bottom>-->
      <!--<v-btn-->
        <!--slot="activator"-->
        <!--color="primary"-->
        <!--dark-->
        <!--fab-->
      <!--&gt;-->
        <!--<v-icon>edit</v-icon>-->
        <!--<v-icon>close</v-icon>-->
      <!--</v-btn>-->
    <!--</v-speed-dial>-->
  </v-container>
</template>

<script>
  import Vue from 'vue'
  import * as d3 from 'd3'
  import * as d3color from 'd3-scale-chromatic'

  import {webSocketServerUrl, } from './../main'

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
        var ws = this.ws;

        var color = d3color.schemeCategory10;
        var colorMapping = {0: color[5]};
        var radius = 10;

        d3.selectAll("#svg-graph > *").remove();

        var svg = d3.select("#svg-graph"),
            width = +svg.attr("width"),
            height = +svg.attr("height");

        var simulation = d3.forceSimulation()
					.nodes(this.graphData.nodes);

        var link_force =  d3.forceLink(this.graphData.links).id(function(d) { return d.id});
        var charge_force = d3.forceManyBody().strength(-13000);
        var center_force = d3.forceCenter(width / 2, height / 2);

        simulation
          .force("charge_force", charge_force)
          .force("center_force", center_force)
          .force("links", link_force);

        simulation.on("tick", tickActions );

        var g = svg.append("g")
          .attr("class", "everything");

        var link = g.append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(this.graphData.links)
          .enter().append("line")
          .attr("stroke-width", 8)
          .attr("stroke-opacity", 0.6)
          .on("mousedown", function(event){
              var move_request = {
                type: 'MSG_MOVE',
                start_node: event.source.index,
                end_node: event.target.index
              };
              ws.send(JSON.stringify(move_request));
            })
          .style("stroke", linkColour);

        var node = g.append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(this.graphData.nodes)
          .enter()
          .append("circle")
          .attr("r", radius)
          .attr("fill", circleColour);


        var drag_handler = d3.drag()
          .on("start", drag_start)
          .on("drag", drag_drag)
          .on("end", drag_end);
        drag_handler(node);

        var zoom_handler = d3.zoom()
          .on("zoom", zoom_actions);

        zoom_handler(svg);

        function circleColour(d){
          return "cadetblue"
        }

        function colorFromUUID(uuid) {
          var mappedColor = colorMapping[uuid];
          if (mappedColor === undefined){
            mappedColor = color[Object.keys(colorMapping).length + 1];
            colorMapping[uuid] = mappedColor;
          }
          return mappedColor;
        }

        function linkColour(d){
          return colorFromUUID(d.player);
        }

        function drag_start(d) {
         if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function drag_drag(d) {
          d.fx = d3.event.x;
          d.fy = d3.event.y;
        }

        function drag_end(d) {
          if (!d3.event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }

        function zoom_actions(){
            g.attr("transform", d3.event.transform)
        }

        function tickActions() {
           node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

          link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        }

      },
      webSocketConnection: function() {
        var gameComponent = this;
        var messageCounter = 0;
        this.ws = new WebSocket(
          webSocketServerUrl + 'game/' + this.$route.params.roomId
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
      },
    },
    mounted () {
      this.webSocketConnection();
      this.renderGraph();
    },
    watch: {
      graphData: {
        handler: 'renderGraph',
        deep: true
      }
    },
  })
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .links line {
      stroke: #FFFFFF;
      stroke-opacity: 0.6;
    }

    .nodes text {
      stroke: #ffffff
    }

    .nodes circle {
      stroke: black	;
      stroke-width: 0px;
    }

</style>
