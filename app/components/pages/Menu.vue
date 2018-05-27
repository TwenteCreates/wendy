<template>
	<section>
		<header>
			Menu
		</header>
		<main>
			<ul>
				<li>
					<a target="_blank" href="https://github.com/AnandChowdhary/dutch-open-hack">
						<i class="fab fa-fw fa-github"></i>
						GitHub repo
					</a>
				</li>
			</ul>
			<h2 class="subtitle">Advanced</h2>
			<ul>
				<li>
					<button @click="clearClassifier">
						<i class="fas fa-fw fa-ban"></i>
						Clear classifier data
					</button>
				</li>
				<li>
					<button @click="clearClassifier">
						<i class="fas fa-fw fa-user-times"></i>
						Load Missing Persons data
					</button>
				</li>
				<li>
					<button @click="clearClassifier">
						<i class="fas fa-fw fa-user-ninja"></i>
						Load Wanted Persons data
					</button>
				</li>
				<li>
					<button @click="clearClassifier">
						<i class="fas fa-fw fa-robot"></i>
						Retrain classifier data
					</button>
				</li>
				<li>
					<button @click="clearClassifier">
						<i class="fas fa-fw fa-envelope"></i>
						Send sample SMS
					</button>
				</li>
				<li>
					<router-link to="/404">
						<i class="fas fa-fw fa-exclamation-triangle"></i>
						404 page
					</router-link>
				</li>
			</ul>
		</main>
	</section>
</template>

<script>
export default {
	methods: {
		clearClassifier() {}
	}
};
</script>


<style lang="scss" scoped>
ul {
	margin: 1rem 0 0 0;
	padding: 0;
	list-style: none;
	li {
		button,
		a {
			color: inherit;
			font: inherit;
			font-size: 110%;
			box-sizing: border-box;
			padding: 1rem;
			border: none;
			background: #fff;
			border-top: 1px solid #eee;
			box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
			border-radius: 0;
			display: block;
			width: 100%;
			text-align: left;
			i {
				margin-right: 0.75rem;
				color: #999;
			}
		}
	}
}
.agastya--night ul li button,
.agastya--night ul li a {
	background-color: #000;
	border-color: #222;
	box-shadow: 0 0.5rem 1rem rgba(255, 255, 255, 0.2);
}
h2 {
	margin-left: 1rem;
}
</style>
