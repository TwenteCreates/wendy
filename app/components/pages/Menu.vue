<template>
	<section>
		<header>
			Menu
			<i v-if="loading" class="fas fa-sync fa-spin"></i>
		</header>
		<main>
			<ul>
				<li>
					<button @click="deleteEverything">
						<i class="fas fa-fw fa-trash"></i>
						Delete all my data
					</button>
				</li>
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
					<button @click="loadMissingPersons">
						<i class="fas fa-fw fa-user-times"></i>
						Load Missing Persons data
					</button>
				</li>
				<li>
					<button @click="loadWantedPersons">
						<i class="fas fa-fw fa-user-ninja"></i>
						Load Wanted Persons data
					</button>
				</li>
				<li>
					<button @click="trainClassifier">
						<i class="fas fa-fw fa-robot"></i>
						Retrain classifier data
					</button>
				</li>
				<li>
					<button @click="sendSms">
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
import "../../modules/firebase";
import firebase from "firebase";
const database = firebase.database();
export default {
	data() {
		return {
			loading: false
		};
	},
	methods: {
		deleteEverything() {
			this.loading = true;
			fetch(
				"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/delete-collection/final"
			)
				.then(() => {})
				.catch(() => {})
				.then(() => {
					fetch(
						"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/create-collection/final"
					)
						.then(() => {})
						.catch(() => {})
						.then(() => {
							const messages = firebase.database().ref("/");
							messages.once("value").then(snapshot => {
								if (snapshot.val()) {
									const people = snapshot.val().rings || {};
									for (let image in people) {
										const url = people[image].url
											.replace(
												"https://firebasestorage.googleapis.com/v0/b/talanx-hack.appspot.com/o/people%2F",
												""
											)
											.split("?alt=media")[0];
										const imageReference = firebase
											.storage()
											.ref("/")
											.child(`people/${url}`);
										imageReference
											.delete()
											.then(() => {
												console.log("deleted");
											})
											.catch(function(error) {});
										firebase
											.database()
											.ref("/")
											.set({});
									}
								}
							});
							this.loading = false;
						});
				});
		},
		clearClassifier() {
			this.loading = true;
			fetch(
				"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/delete-collection/final"
			)
				.then(() => {})
				.catch(() => {})
				.then(() => {
					fetch(
						"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/create-collection/final"
					)
						.then(() => {})
						.catch(() => {})
						.then(() => {
							this.loading = false;
						});
				});
		},
		loadMissingPersons() {
			this.loading = true;
			fetch(
				"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/load-missing-person-data/final"
			)
				.then(() => {})
				.catch(() => {})
				.then(() => {
					this.loading = false;
				});
		},
		loadWantedPersons() {
			this.loading = true;
			fetch(
				"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/load-fugitive-person-data/final"
			)
				.then(() => {})
				.catch(() => {})
				.then(() => {
					this.loading = false;
				});
		},
		trainClassifier() {
			this.loading = true;
			fetch(
				"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/train-collection/final"
			)
				.then(() => {})
				.catch(() => {})
				.then(() => {
					this.loading = false;
				});
		},
		sendSms() {
			this.loading = true;
			fetch("https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/send-sms", {
				method: "POST",
				headers: {
					"content-type": "application/json"
				},
				body: JSON.stringify({
					messages: [
						{
							content: "Sample message from Wendy",
							mobile_number: "0644691056"
						}
					],
					sender: "Wendy"
				})
			})
				.then(() => {})
				.catch(() => {})
				.then(() => {
					this.loading = false;
				});
		}
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
header .fa-sync {
	position: absolute;
	top: 1.2rem;
	right: 1rem;
}
</style>
