import Vue from "vue";
import VueRouter from "vue-router";

import Chat from "../components/pages/Chat.vue";
import Bell from "../components/pages/Bell.vue";
import People from "../components/pages/People.vue";
import Session from "../components/pages/Session.vue";
import Open from "../components/pages/Open.vue";
import Error404 from "../components/pages/Error404.vue";

const routes = [
	{
		path: "/bell",
		component: Bell
	},
	{
		path: "/chat",
		component: Chat
	},
	{
		path: "/people",
		component: People
	},
	{
		path: "/session/:id",
		component: Session
	},
	{
		path: "/open",
		component: Open
	},
	{
		path: "*",
		component: Error404
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
