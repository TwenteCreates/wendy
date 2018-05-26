<template>
	<nav class="navbar">
		<ul>
			<li>
				<router-link to="/menu">
					<div><i class="fas fa-bars"></i></div>
					<div>Menu</div>
				</router-link>
			</li>
			<li>
				<router-link to="/chat">
					<div><i class="fas fa-robot"></i></div>
					<div>Wendy</div>
				</router-link>
			</li>
			<li>
				<router-link to="/people">
					<div><i class="fas fa-users"></i></div>
					<div>People</div>
				</router-link>
			</li>
			<li>
				<a onclick="window.agastya.open()">
					<div><i class="fas fa-universal-access"></i></div>
					<div>Access</div>
				</a>
			</li>
		</ul>
	</nav>
</template>


<style lang="scss" scoped>
.navbar {
	background-color: #fff;
	box-shadow: 0 -0.5rem 1rem rgba(0, 100, 100, 0.1);
	z-index: 999;
	i {
		font-size: 165%;
	}
	ul {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		li {
			width: 100%;
			text-align: center;
			a {
				color: inherit;
				transition: 0.3s;
				font-size: 80%;
				display: block;
				padding: 0.5rem 0 0.25rem 0;
				opacity: 0.75;
				text-decoration: none;
				svg {
					font-size: 150%;
				}
				&.router-link-exact-active {
					color: #5352ed;
					opacity: 1;
				}
			}
		}
	}
}
</style>
