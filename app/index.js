import Vue from "vue";
import "./pwa";
import router from "./modules/router";

import css from "./app.scss";
import Nav from "./components/Nav.vue";

// import agastya from "@oswaldlabs/agastya";
// window.a11ySettings = window.a11ySettings || {};
// window.a11ySettings.token = "5rlsghx";
// window.a11ySettings.display = "none";

const app = new Vue({
	el: "#app",
	router,
	render() {
		return (
			<div class="app-container">
				<transition name="fade" mode="out-in">
					<router-view />
				</transition>
				<Nav />
			</div>
		);
	}
});
