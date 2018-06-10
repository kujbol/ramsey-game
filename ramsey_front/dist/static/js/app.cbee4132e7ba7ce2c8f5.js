webpackJsonp([1],{"7zck":function(e,t){},NHnr:function(e,t,a){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=a("7+uW"),i=a("/ocq"),r=a("Gu7T"),s=a.n(r),o=a("W3Iv"),l=a.n(o),c=a("BO1k"),u=a.n(c),d=a("d7EF"),v=a.n(d),m=a("fZjL"),p=a.n(m),f=a("mvHQ"),g=a.n(f),h=a("vwbq"),_=a("3wEs"),y=n.a.extend({name:"Game",data:function(){return{ws:null,graphData:{nodes:[],links:[]},dialog:!0,alerts:[]}},methods:{renderGraph:function(){var e=this.ws,t=_.a,a={0:t[5]};h.h("#svg-graph > *").remove();var n=h.g("#svg-graph"),i=+n.attr("width"),r=+n.attr("height"),s=h.f().nodes(this.graphData.nodes),o=h.d(this.graphData.links).id(function(e){return e.id}),l=h.e().strength(-12e3).distanceMax(1500).distanceMin(400),c=h.c(i/2,r/2);s.force("charge_force",l).force("center_force",c).force("links",o),s.on("tick",function(){v.attr("cx",function(e){return e.x}).attr("cy",function(e){return e.y}),d.attr("x1",function(e){return e.source.x}).attr("y1",function(e){return e.source.y}).attr("x2",function(e){return e.target.x}).attr("y2",function(e){return e.target.y})});var u=n.append("g").attr("class","everything"),d=u.append("g").attr("class","links").selectAll("line").data(this.graphData.links).enter().append("line").attr("stroke-width",8).attr("stroke-opacity",.6).on("mousedown",function(t){var a={type:"MSG_MOVE",start_node:t.source.index,end_node:t.target.index};e.send(g()(a))}).style("stroke",function(e){return function(e){var n=a[e];void 0===n&&(n=t[p()(a).length+1],a[e]=n);return n}(e.player)}),v=u.append("g").attr("class","nodes").selectAll("circle").data(this.graphData.nodes).enter().append("circle").attr("r",10).attr("fill",function(e){return"cadetblue"});h.a().on("start",function(e){h.b.active||s.alphaTarget(.3).restart();e.fx=e.x,e.fy=e.y}).on("drag",function(e){e.fx=h.b.x,e.fy=h.b.y}).on("end",function(e){h.b.active||s.alphaTarget(0);e.fx=null,e.fy=null})(v),h.i().on("zoom",function(){u.attr("transform",h.b.transform)})(n)},webSocketConnection:function(){var e=this,t=0;this.ws=new WebSocket($+"game/"+this.$route.params.roomId),this.ws.addEventListener("open",function(e){this.send(g()({type:"MSG_CONNECT"}))}),this.ws.addEventListener("message",function(a){var n=JSON.parse(a.data);if(console.log(n),"MSG_GAME"===n.type){e.$data.dialog=!1;var i=n.body.available_graph,r=!0,o=!1,c=void 0;try{for(var d,m=u()(i.links);!(r=(d=m.next()).done);r=!0){d.value.player=0}}catch(e){o=!0,c=e}finally{try{!r&&m.return&&m.return()}finally{if(o)throw c}}var p=!0,f=!1,g=void 0;try{for(var h,_=u()(l()(n.body.players_graph));!(p=(h=_.next()).done);p=!0){for(var y,b=h.value,x=v()(b,2),w=x[0],k=x[1],z=0;z<k.links.length;z++)k.links[z].player=w;(y=i.links).push.apply(y,s()(k.links))}}catch(e){f=!0,g=e}finally{try{!p&&_.return&&_.return()}finally{if(f)throw g}}e.graphData=i,e.renderGraph()}if("MSG_MOVE"===n.type){var S=n.body.start_node,G=n.body.end_node,q=n.player,C=e.graphData.links.filter(function(e){return e.source.id==S&&e.target.id==G||e.target.id==S&&e.source.id==G});console.log(C),C[0].player=q}"MSG_INFO"===n.type&&(t+=1,e.$data.alerts.push({type:"info",details:n.body.details,id:t,open:!0})),"MSG_ERROR"===n.type&&(t+=1,e.$data.alerts.push({type:"error",details:n.body.details,id:t,open:!0})),"MSG_WON"===n.type&&(t+=1,e.$data.alerts.push({type:"success",details:n.body.details,id:t,open:!0}))})}},mounted:function(){this.webSocketConnection()},watch:{graphData:{handler:"renderGraph",deep:!0}}}),b={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",{attrs:{fluid:"","fill-height":""}},[a("v-layout",{attrs:{"justify-center":"","align-center":"","fill-height":""}},[a("v-flex",{attrs:{"d-flex":""}},[a("v-container",{attrs:{id:"main-container"}},[e._l(e.alerts,function(t){return a("v-alert",{key:t.id,attrs:{color:t.type,icon:t.type,transition:"scale-transition",dismissible:""},model:{value:t.open,callback:function(a){e.$set(t,"open",a)},expression:"alert.open"}},[e._v("\n          "+e._s(t.details)+"\n        ")])}),e._v(" "),a("v-slide-y-transition",{attrs:{mode:"out-in"}},[a("v-layout",{attrs:{column:"","align-center":""}},[a("svg",{attrs:{id:"svg-graph",width:"1500",height:"630"}},[a("g",{staticClass:"links"}),e._v(" "),a("g",{staticClass:"nodes"})])])],1),e._v(" "),a("v-dialog",{attrs:{persistent:"","max-width":"380"},model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[a("v-card",[a("v-card-title",{staticClass:"headline"},[e._v("Waiting for other players to join")]),e._v(" "),a("v-card-text",[a("v-layout",{attrs:{"align-center":"","justify-center":""}},[a("v-progress-circular",{attrs:{indeterminate:"",color:"primary"}})],1)],1)],1)],1)],2)],1)],1)],1)},staticRenderFns:[]};var x=a("VU/8")(y,b,!1,function(e){a("qzN+")},"data-v-e0f812c4",null).exports,w=a("mtWM"),k=a.n(w),z={name:"NewGameDialog",props:["visible"],computed:{show:{get:function(){return this.visible},set:function(e){e||this.$emit("close")}}},data:function(){return{valid:!1,nameRules:[function(e){return!!e||"Name is required"},function(e){return e.length<=10||"Name must be less than 10 characters"}],name:"",gameSize:"7",gameSizeRules:[function(e){return!!e||"Game size is required"},function(e){return/^\d+$/.test(e)||"Expected number"},function(e){return e<=100||"Game size must be less than 100"}],cliqueSize:"3",cliqueSizeRules:[function(e){return!!e||"Game size is required"},function(e){return/^\d+$/.test(e)||"Expected number"},function(e){return e<=100||"Game size must be less than 100"}],aiPlayer:!1}},methods:{submit:function(){var e={data:{game_name:this.name,graph_size:this.gameSize,clique_size:this.cliqueSize,is_ai:this.aiPlayer}};k.a.post(M+"games",e,{headers:{"Access-Control-Allow-Origin":"*"}}).then(this.$emit("submitted"))}}},S={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-dialog",{attrs:{"max-width":"450"},model:{value:e.show,callback:function(t){e.show=t},expression:"show"}},[a("v-container",[a("v-form",{model:{value:e.valid,callback:function(t){e.valid=t},expression:"valid"}},[a("v-text-field",{attrs:{counter:10,rules:e.nameRules,label:"Name",required:""},model:{value:e.name,callback:function(t){e.name=t},expression:"name"}}),e._v(" "),a("v-text-field",{attrs:{label:"Game Size",rules:e.gameSizeRules,required:""},model:{value:e.gameSize,callback:function(t){e.gameSize=t},expression:"gameSize"}}),e._v(" "),a("v-text-field",{attrs:{label:"Winning clique Size",rules:e.cliqueSizeRules,required:""},model:{value:e.cliqueSize,callback:function(t){e.cliqueSize=t},expression:"cliqueSize"}}),e._v(" "),a("v-checkbox",{attrs:{label:"Is Ai player"},model:{value:e.aiPlayer,callback:function(t){e.aiPlayer=t},expression:"aiPlayer"}}),e._v(" "),a("v-btn",{attrs:{disabled:!e.valid},on:{click:e.submit}},[e._v("\n        submit\n      ")]),e._v(" "),a("v-btn",{attrs:{color:"error"},on:{click:function(t){t.stopPropagation(),e.show=!1}}},[e._v("close")])],1)],1)],1)},staticRenderFns:[]};var G=a("VU/8")(z,S,!1,function(e){a("t+4e")},"data-v-ea102d24",null).exports,q={name:"GameList",components:{"new-game-dialog":G},data:function(){return{newGameDialog:!1,games:[],headers:[{text:"Id",value:"id"},{text:"Name",value:"name"},{text:"State",value:"state"},{text:"Graph size",value:"size"},{text:"Clique size",value:"finish_size"},{text:"Players",value:"player_count"},{text:"Join game",value:"join_game",sortable:!1}]}},mounted:function(){this.loadList()},methods:{loadList:function(){var e=this;k.a.get(M+"games",{headers:{"Access-Control-Allow-Origin":"*"}}).then(function(t){e.games=t.data.data.games,setTimeout(e.loadList,2e3)})},submitted:function(){var e=this;this.newGameDialog=!1,k.a.get(M+"games",{headers:{"Access-Control-Allow-Origin":"*"}}).then(function(t){e.games=t.data.data.games})}}},C={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-container",{attrs:{fluid:""}},[a("v-data-table",{staticClass:"elevation-5",attrs:{headers:e.headers,items:e.games,"hide-actions":""},scopedSlots:e._u([{key:"items",fn:function(t){return[a("td",[e._v(e._s(t.item.id))]),e._v(" "),a("td",[e._v(e._s(t.item.name))]),e._v(" "),a("td",[e._v(e._s(t.item.state))]),e._v(" "),a("td",[e._v(e._s(t.item.size))]),e._v(" "),a("td",[e._v(e._s(t.item.finish_size))]),e._v(" "),a("td",[e._v(e._s(t.item.player_count))]),e._v(" "),a("td",[a("v-btn",{staticClass:"mx-0",attrs:{icon:"",to:{name:"game",params:{roomId:t.item.id}}}},[a("v-icon",{attrs:{color:"primary"}},[e._v("mouse")])],1)],1)]}}])}),e._v(" "),a("v-btn",{attrs:{color:"primary"},on:{click:function(t){t.stopPropagation(),e.newGameDialog=!0}}},[e._v("Create Game")]),e._v(" "),a("new-game-dialog",{attrs:{visible:e.newGameDialog},on:{close:function(t){e.newGameDialog=!1},submitted:function(t){e.submitted()}}})],1)},staticRenderFns:[]};var E=a("VU/8")(q,C,!1,function(e){a("oaaT")},"data-v-db97a068",null).exports;n.a.use(i.a);var D=new i.a({routes:[{path:"/game/:roomId",name:"game",component:x},{path:"/",name:"game_list",component:E}]}),N=a("3EgV"),R=a.n(N),A={render:function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("v-app",{attrs:{id:"inspire",dark:""}},[a("v-navigation-drawer",{attrs:{clipped:"",fixed:"",app:""},model:{value:e.drawer,callback:function(t){e.drawer=t},expression:"drawer"}},[a("v-list",{attrs:{dense:""}},[a("v-list-tile",{on:{click:function(e){}}},[a("v-list-tile-action",[a("v-icon",[e._v("dashboard")])],1),e._v(" "),a("v-list-tile-content",[a("router-link",{attrs:{to:{name:"game_list"}}},[e._v("Rooms")])],1)],1),e._v(" "),a("v-list-tile",{on:{click:function(e){}}},[a("v-list-tile-action",[a("v-icon",[e._v("settings")])],1),e._v(" "),a("v-list-tile-content",[a("v-list-tile-title",[e._v("Settings")])],1)],1)],1)],1),e._v(" "),a("v-toolbar",{attrs:{app:"",fixed:"","clipped-left":""}},[a("v-toolbar-side-icon",{on:{click:function(t){t.stopPropagation(),e.drawer=!e.drawer}}}),e._v(" "),a("v-toolbar-title",[e._v("Ramsey Game")])],1),e._v(" "),a("v-content",[a("router-view")],1)],1)},staticRenderFns:[]},F=a("VU/8")({data:function(){return{drawer:!1,fixed:!1,title:"Vuetify.js"}},name:"App"},A,!1,null,null,null).exports;a("7zck");a.d(t,"serverUrl",function(){return M}),a.d(t,"webSocketServerUrl",function(){return $});var M="http://ramsey-game.herokuapp.com/",$="ws://ramsey-game.herokuapp.com/";n.a.use(R.a,{theme:{primary:"#ee44aa",secondary:"#424242",accent:"#82B1FF",error:"#FF5252",info:"#2196F3",success:"#4CAF50",warning:"#FFC107"}}),n.a.config.productionTip=!1,new n.a({el:"#app",router:D,components:{App:F,NewGameDialog:G,GameList:E},template:"<App/>"})},oaaT:function(e,t){},"qzN+":function(e,t){},"t+4e":function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.cbee4132e7ba7ce2c8f5.js.map