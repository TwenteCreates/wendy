<template>
	<section>
		<header>
			<router-link class="back-button" to="/people">
				<i class="fas fa-arrow-left"></i>
			</router-link>
			Details
		</header>
		<main class="session">
			<h2 class="subtitle">Profile</h2>
			<div class="item tc">
				<div class="img" :style="`background: url('${session.url}') center center / cover no-repeat`"></div>
				<div class="griddy">
					<div>
						<div><strong>{{session.name || "Unknown name"}}</strong></div>
						<div class="light">{{format(id)}}</div>
					</div>
				</div>
				<div class="session-status">
					<div v-if="session.userData === `trusted`">
						<i class="fas fa-check-circle"></i>
						Trusted
					</div>
					<div v-else-if="session.userData === `missing`">
						<i class="fas fa-exclamation-circle"></i>
						Missing
					</div>
					<div v-else-if="session.userData === `wanted`">
						<i class="fas fa-exclamation-circle"></i>
						Wanted
					</div>
					<div v-else>
						<i class="fas fa-times-circle"></i>
						Not trusted
					</div>
				</div>
			</div>
			<h2 class="subtitle">Labels</h2>
			<div class="item" v-for="(classification, id) in session.kpn" :key="`classification${id}`" v-if="id < 3">
				<div class="griddy">
					<div class="img" :style="`background: url('https://tse2.mm.bing.net/th?q=${classification.classification}&w=400&h=300&p=0&dpr=2&adlt=moderate&c=1') center center / cover no-repeat`"></div>
					<div>
						<div><strong>{{sentenceCase(classification.classification)}}</strong></div>
						<div class="light">{{parseInt(classification.score * 100)}}% confidence</div>
					</div>
				</div>
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
			id: "",
			session: {}
		};
	},
	methods: {
		format(date) {
			return moment.unix(date / 1000).format("MMMM D, YYYY H:mm a");
		},
		sentenceCase(word) {
			return sentenceCase(word);
		}
	},
	mounted() {
		this.id = this.$route.params.id;
		const session = firebase.database().ref(`/rings/${this.id}`);
		session.once("value").then(snapshot => {
			this.session = snapshot.val() || [];
		});
		session.on("value", snapshot => {
			if (snapshot.val() && (snapshot.val() || []).length > 0) {
				this.session = snapshot.val();
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
		justify-content: space-between;
		i {
			margin-right: 0.5rem;
		}
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
.tc {
	align-items: center;
	display: flex;
	flex-direction: column;
	text-align: center;
	.img {
		margin-right: 0;
		margin-bottom: 1rem;
		height: 100px;
		width: 100px;
	}
}
i.fa-check-circle {
	color: #2ecc71;
}
i.fa-exclamation-circle {
	color: #e74c3c;
}
i.fa-times-circle {
	color: #f39c12;
}
.session-status {
	font-weight: bold;
	margin-top: 0.5rem;
	font-size: 125%;
}
</style>
