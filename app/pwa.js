import runtime from "offline-plugin/runtime";

if (process.env.NODE_ENV === "production") {
	runtime.install({
		onUpdateReady() {
			runtime.applyUpdate();
		},
		onUpdated() {
			location.reload();
		}
	});
}
