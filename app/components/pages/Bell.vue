<template>
	<div>
		<webcam ref="webcam" :width="width"></webcam>
		<nav>NAV</nav>
	</div>
</template>

<script>
import Webcam from "vue-web-cam/src/webcam";
export default {
	data() {
		return {
			width: 100
		};
	},
	mounted() {
		this.width = window.innerWidth;
	},
	components: {
		Webcam
	}
};
</script>


<style lang="scss" scoped>
</style>
