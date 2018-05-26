<template>
	<section>
		<header>
			People
		</header>
		<main class="people">
			<div class="item" v-for="(person, id) in people" :key="`person${id}`">
				<div class="griddy">
					<div class="img" :style="`background: url('${person.url}') no-repeat center; background-size: cover`"></div>
					<div>
						<div><strong>Anand Chowdhary</strong></div>
						<div class="light">{{format(id)}}</div>
					</div>
				</div>
				<footer>
					<div>
						<i class="fas fa-check-circle"></i>Safe
					</div>
				</footer>
			</div>
		</main>
	</section>
</template>

<script>
import moment from "moment";
import "../../modules/firebase";
import firebase from "firebase";
import sentenceCase from "sentence-case";
const database = firebase.database();
export default {
	data() {
		return {
			people: []
		};
	},
	methods: {
		format(date) {
			return moment.unix(date / 1000).format("MMMM D, YYYY H:mm a");
		}
	},
	mounted() {
		const people = firebase.database().ref(`/rings`);
		people.once("value").then(snapshot => {
			this.people = snapshot.val() || [];
		});
		people.on("value", snapshot => {
			if (snapshot.val() && (snapshot.val() || []).length > 0) {
				this.people = snapshot.val();
			}
		});
	}
};
</script>


<style lang="scss" scoped>
main {
	padding: 1rem;
}
.item {
	background-color: #ffffff;
	padding: 0.75rem 1rem;
	box-shadow: 0 0.5rem 1rem rgba(0, 100, 100, 0.1);
	border-radius: 0.25rem;
	.griddy,
	footer {
		display: flex;
		align-items: center;
	}
	footer {
		margin-top: 0.75rem;
	}
	margin-bottom: 1rem;
	.img {
		border-radius: 100%;
		width: 50px;
		height: 50px;
		margin-right: 1rem;
		background-color: #aaa;
	}
	.light {
		color: #999;
	}
}
i.fa-check-circle {
	color: #2ecc71;
	margin-right: 0.5rem;
}
</style>
