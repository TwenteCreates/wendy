const OfflinePlugin = require("offline-plugin");
const sass = require("node-sass");
const moduleImporter = require("sass-npm-import");

module.exports = options => ({
	entry: "./index.js",
	babel: {
		jsx: "vue"
	},
	extendWebpack(config) {
		if (options.mode === "production") {
			config.plugin("offline").use(OfflinePlugin);
		}
		sass.render(
			{
				file: "./app.scss",
				importer: moduleImporter()
			},
			() => {}
		);
	},
	html: {
		template: "./template.ejs"
	}
});
