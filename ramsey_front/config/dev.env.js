'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  SERVER_URl: "'http://0.0.0.0:8000/'",
  WS_SERVER_URL: "'ws://0.0.0.0:8000/'"
})
