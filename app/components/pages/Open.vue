<template>
	<section>
		<main class="success">
			<i class="fas fa-check-circle"></i>
		</main>
	</section>
</template>

<script>
export default {
	mounted() {
		setTimeout(() => {
			this.$router.push("/bell");
		}, 5000);
	}
};
</script>


<style lang="scss" scoped>
.success {
	position: fixed;
	background-color: #2ecc71;
	color: #fff;
	left: 0;
	right: 0;
	top: 0;
	bottom: 0;
	text-align: center;
	padding-top: 35vh;
	font-size: 20vh;
	z-index: 1000;
}
</style>
