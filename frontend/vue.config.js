/* eslint-disable */
const path = require("path");
const { gitDescribeSync } = require("git-describe");

const gitInfo = gitDescribeSync();

process.env.VUE_APP_VERSION = gitInfo.distance ? gitInfo.raw : gitInfo.tag;

module.exports = {
  outputDir: "../frontend_assets",
  assetsDir: "static",

  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "~@/styles/variables"`,
      },
      scss: {
        additionalData: `@import "~@/styles/variables";`,
      },
    },
  },
  
  devServer: {
    proxy: {
      "/api*": {
        // Forward frontend dev server request for /api to django dev server
        target: "http://localhost:8000/",
      },
      "/admin-*": {
        // Forward frontend dev server request for /api to django dev server
        target: "http://localhost:8000/",
      },
    },
  },

};
