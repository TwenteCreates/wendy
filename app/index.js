import Vue from "vue";
import "./pwa";
import router from "./modules/router";

import css from "./app.scss";

const app = new Vue({
	el: "#app",
	router,
	render() {
		return (
			<div>
				<transition name="fade" mode="out-in">
					<router-view />
				</transition>
			</div>
		);
	}
});