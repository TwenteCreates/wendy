import Vue from "vue";
import VueRouter from "vue-router";

import Error404 from "../components/pages/Error404.vue";

const routes = [
	{
		path: "*",
		component: Error404,
		meta: {
			title: "404 Error"
		}
	}
];

Vue.use(VueRouter);
const router = new VueRouter({
	routes,
	mode: "history",
	scrollBehavior(to, from, savedPosition) {
		// Scroll to top when animation is complete
		return new Promise((resolve, reject) => {
			setTimeout(() => {
				resolve(
					savedPosition || {
						x: 0,
						y: 0
					}
				);
			}, 200);
		});
	}
});

export default router;