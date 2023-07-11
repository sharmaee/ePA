/* eslint-disable */
const path = require("path");
const { gitDescribeSync } = require("git-describe");

const gitInfo = gitDescribeSync();

process.env.VUE_APP_VERSION = gitInfo.distance ? gitInfo.raw : gitInfo.tag;

module.exports = {
  outputDir: "../frontend_assets",
  transpileDependencies: true,

  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "~@/styles/variables"`,
      },
      scss: {
        additionalData: `@import "~@/styles/variables";`,
      },
    },
  }
};
