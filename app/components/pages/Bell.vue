<template>
	<section>
		<main>
			<webcam ref="webcam" :width="width" :height="height"></webcam>
		</main>
		<footer class="ring">
			<div class="buttons">
				<button>
					<i class="fas fa-fw fa-phone fa-flip-horizontal"></i>
				</button>
				<button class="big">
					<i class="fas fa-fw fa-bell"></i>
				</button>
				<button>
					<i class="fas fa-fw fa-microphone"></i>
				</button>
			</div>
		</footer>
	</section>
</template>


<script>
import Webcam from "vue-web-cam/src/webcam";
export default {
	data() {
		return {
			width: 100,
			height: 100
		};
	},
	mounted() {
		this.width = window.innerWidth;
		this.height = window.innerHeight;
	},
	components: {
		Webcam
	}
};
</script>


<style lang="scss" scoped>
video {
	background-color: #000;
	position: fixed;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	z-index: 1;
	transform: scale(3);
}
footer.ring {
	position: fixed;
	bottom: 0;
	left: -20px;
	right: -20px;
	box-sizing: border-box;
	padding: 0 20px;
	background-color: rgba(100, 100, 100, 0.5);
	backdrop-filter: blur(15px);
	z-index: 5;
}
.buttons {
	display: flex;
	justify-content: space-between;
	button {
		background: none;
		color: #fff;
		border: none;
		padding: 1rem 2rem;
		font: inherit;
		font-size: 1.5rem;
		&.big {
			font-size: 3rem;
		}
	}
}
</style>

<style>
.navbar {
	display: none;
}
</style>
