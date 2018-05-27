<template>
	<section>
		<main>
			<webcam ref="webcam" :width="width"></webcam>
			<transition name="fade" mode="out-in">
				<article class="login" v-show="login">
					<p>Touch your finger or enter pin</p>
					<img alt="Fingerprint" src="/fingerprint.png">
					<div class="pin">
						<button v-for="n in [1, 2, 3, 4, 5, 6, 7, 8, 9, ' ', 0]" :key="`button${n}`">{{ n }}</button>
					</div>
				</article>
			</transition>
		</main>
		<footer class="ring">
			<div class="buttons">
				<button>
					<i class="fas fa-fw fa-phone fa-flip-horizontal"></i>
				</button>
				<button class="big" @click.prevent="ring">
					<i v-if="!bell" class="fas fa-fw fa-bell"></i>
					<i v-else class="fas fa-fw fa-sync fa-spin"></i>
				</button>
				<button @click.prevent="openLogin">
					<i class="fas fa-fw fa-lock"></i>
				</button>
			</div>
		</footer>
	</section>
</template>


<script>
import firebase from "firebase/app";
import "firebase/storage";
import "firebase/database";
import Webcam from "vue-web-cam/src/webcam";
export default {
	data() {
		return {
			width: 100,
			bell: false,
			login: false
		};
	},
	mounted() {
		this.width = window.innerWidth;
		this.height = window.innerHeight;
		const infoStore = firebase.database().ref(`/`);
		infoStore.on("value", snapshot => {
			if (snapshot.val()) {
				if (snapshot.val().access) {
					infoStore.update({
						access: false
					});
					this.$router.push("/open");
				}
			}
		});
	},
	methods: {
		openLogin() {
			this.login = !this.login;
		},
		ring() {
			const audio = new Audio("/bell.mp3");
			audio.play();
			this.bell = true;
			const storageRef = firebase.storage().ref(
				`/people/${Math.random()
					.toString(36)
					.slice(2)}.jpg`
			);
			let array, binary, i;
			binary = atob(this.$refs.webcam.capture().split(",")[1]);
			array = [];
			i = 0;
			while (i < binary.length) {
				array.push(binary.charCodeAt(i));
				i++;
			}
			const picture = new Blob([new Uint8Array(array)], {
				type: "image/jpeg"
			});
			storageRef
				.put(picture)
				.then(snapshot => {
					return snapshot.ref.getDownloadURL();
				})
				.then(url => {
					fetch(
						"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/image-classify",
						{
							method: "POST",
							cors: true,
							body: JSON.stringify({
								urls: [
									{
										ext: "jpg",
										path: url
									}
								]
							})
						}
					)
						.then(response => response.json())
						.then(json => {
							const database = firebase.database();
							database
								.ref()
								.child(`/rings/${new Date().getTime()}`)
								.set({
									url: url,
									kpn: json.results[0].result
								});
							this.bell = false;
						})
						.catch(() => {
							this.bell = false;
						});
				});
		}
	},
	components: {
		Webcam
	}
};
</script>


<style lang="scss" scoped>
section {
	background-color: #000;
}
video {
	background-color: #000;
	position: fixed;
	left: 0;
	right: 0;
	top: 50%;
	transform: translateY(-50%);
	height: auto !important;
	z-index: 1001;
}
footer.ring,
article.login {
	box-sizing: border-box;
	padding: 0 20px;
	background-color: rgba(100, 100, 100, 0.5);
	backdrop-filter: blur(15px);
	z-index: 1005;
	text-align: center;
	position: fixed;
	color: #fff;
}
footer.ring {
	bottom: 0;
	left: -20px;
	right: -20px;
}
article.login {
	top: 0;
	left: -20px;
	right: -20px;
	padding: 40px;
	img {
		margin-top: 1rem;
		max-width: 15%;
	}
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
			font-size: 4rem;
		}
	}
}
.pin {
	margin-top: 2rem;
	button {
		border: none;
		background: none;
		width: 33%;
		float: left;
		font: inherit;
		color: #fff;
		font-size: 1.75rem;
		padding: 0.5rem 0;
	}
	&::after {
		content: "";
		display: block;
		clear: both;
	}
}
</style>
