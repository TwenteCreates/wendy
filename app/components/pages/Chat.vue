<template>
	<section>
		<header>
			<img alt="Wendy" src="/text.png">
		</header>
		<main class="main-chat">
			<div v-for="(message, index) in messages" :key="`message${index}`" v-bind:class="`message-block ${message.sender} next-${message.next || 'none'} previous-${message.previous || 'none'} class-${message.class || 'none'}`">
				<div v-if="message.sender === `meta`" class="message-meta">
					<div class="details">{{message.text}}</div>
				</div>
				<div v-else-if="message.sender === `sender-2`" class="message-content">
					<div class="message">
						<div class="message-inner" v-if="!message.text.includes(`IMAGE_URL|`)">{{message.text}}</div>
						<div class="message-inner inline-image" v-else>
							<img alt="Uploaded image" :src="message.text.replace(`IMAGE_URL|`, ``)">
						</div>
					</div>
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
				</div>
				<div v-else class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="message.avatar">
					</div>
					<div class="message">
						<div class="message-inner" v-if="!message.text.includes(`IMAGE_URL|`)">{{message.text}}</div>
						<div class="message-inner inline-image" v-else>
							<img alt="Uploaded image" :src="message.text.replace(`IMAGE_URL|`, ``)">
						</div>
						<div class="has-attachment" v-if="message.attachment">
							<div>{{message.attachment.accessCode}}</div>
							<div>{{message.attachment.amount.currency}} {{message.attachment.amount.amount}}</div>
							<div><strong>BIC</strong> {{message.attachment.fallbackBankAccount.bic}}</div>
							<div><strong>IBAN</strong> {{message.attachment.fallbackBankAccount.iban}}</div>
						</div>
					</div>
				</div>
			</div>
			<div class="message-block sender-1 typing" v-if="typing">
				<div class="message-content">
					<div class="sender">
						<img alt="Sender's Avatar" :src="currentImage">
						</div>
					<div class="message">
						<div class="message-inner">
							<span class="ellipsis-1">&bullet;</span>
							<span class="ellipsis-2">&bullet;</span>
							<span class="ellipsis-3">&bullet;</span>
						</div>
					</div>
				</div>
			</div>
		</main>
		<footer>
			<transition name="fade" mode="out-in">
				<div class="options" v-if="options.length > 0">
					<ul>
						<li v-for="(option, id) in options" :key="`option_${id}`">
							<button @click="animateButton(option)">{{option}}</button>
						</li>
					</ul>
				</div>
			</transition>
			<div class="reply-box">
				<form @submit.prevent="sendMessage">
					<input type="text" v-model="reply" @keyup="textChanged" placeholder="Enter a message...">
					<button type="button" v-if="!speaking" @click="startSpeech">
						<i class="fas fa-fw fa-microphone"></i>
					</button>
					<button type="button" v-else>
						<i class="fas fa-fw fa-signal"></i>
					</button>
					<button type="submit">
						<i class="fas fa-fw fa-arrow-right"></i>
					</button>
				</form>
			</div>
		</footer>
	</section>
</template>

<script>
import "../../modules/firebase";
import firebase from "firebase";
import sentenceCase from "sentence-case";
const database = firebase.database();
let lastImage = null;
let recentlyDone = false;
function getOffset(el) {
	var _x = 0;
	var _y = 0;
	while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
		_x += el.offsetLeft - el.scrollLeft;
		_y += el.offsetTop - el.scrollTop;
		el = el.offsetParent;
	}
	return { top: _y, left: _x };
}
export default {
	mounted() {
		const messages = firebase.database().ref(`/`);
		messages.once("value").then(snapshot => {
			if (snapshot.val()) {
				this.messages = snapshot.val().conversation || [];
				this.people = snapshot.val().rings || [];
			}
			if (!snapshot.val() || (snapshot.val().conversation || []).length === 0) {
				this.botSays(`Hi 👋`);
				setTimeout(() => {
					this.botSays(`Everything looks good at home!`);
				}, 200);
				setTimeout(() => {
					this.botSays(`How can I help?`, [
						"Hi",
						"People who visited recently",
						"Security report"
					]);
				}, 400);
			} else {
				this.options =
					snapshot.val().conversation[snapshot.val().conversation.length - 1].options ||
					[];
			}
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
		});
		messages.on("value", snapshot => {
			if (snapshot.val()) {
				if (snapshot.val().rings) {
					if (
						Object.keys(snapshot.val().rings).length !== 1 &&
						Object.keys(snapshot.val().rings).length -
							Object.keys(this.people).length ==
							1 &&
						!recentlyDone
					) {
						this.people = snapshot.val().rings;
						const currPersonId = Object.keys(this.people)[
							Object.keys(this.people).length - 1
						];
						if (this.people[currPersonId].userData) {
							this.botSays(
								`Hey, just to keep you posted: ${
									this.people[currPersonId].name
								} is home.`
							);
						} else {
							recentlyDone = true;
							setTimeout(() => {
								recentlyDone = false;
							}, 1000);
							this.botSays(`There's someone at the door.`);
							this.botSays(`It's not in your trusted contacts.`);
							this.botSays("IMAGE_URL|" + this.people[currPersonId].url);
							lastImage = currPersonId;
							this.botSays(`What do you want to do?`, [
								"Unlock door",
								"Ignore",
								"Start call"
							]);
						}
					}
				}
				if (
					snapshot.val() &&
					snapshot.val().conversation &&
					(snapshot.val().conversation || []).length > 0
				) {
					if (
						!!snapshot.val().conversation[snapshot.val().conversation.length - 1]
							.botShould
					) {
						this.respond(
							snapshot.val().conversation[snapshot.val().conversation.length - 1].text
						)
							.then(response => {
								this.respondResponse(response);
							})
							.catch(() => {});
					}
					this.messages = snapshot.val().conversation || [];
					setTimeout(() => {
						this.$el.querySelector("main").scrollTop = this.$el.querySelector(
							"main"
						).scrollHeight;
					}, 1);
					this.messages.forEach(message => {
						if (message.text === "Isabella has joined the conversation") {
							this.bossHasJoined = true;
						}
					});
				}
			}
		});
	},
	data: () => {
		return {
			currentImage: "/bot.png",
			typing: false,
			imageUrl: "",
			reply: "",
			speaking: false,
			messages: [],
			voice: null,
			options: [],
			nextMessages: [],
			currentQ: null,
			bossHasJoined: false,
			people: [],
			contexts: null
		};
	},
	methods: {
		textChanged() {
			if (this.currentQ === "place_name" && this.reply.trim().length > 0) {
			}
		},
		saveMessages() {
			database.ref(`/conversation`).set(this.messages);
		},
		animateButton(text) {
			if (!this.messages) return;
			if (text === "Click photo") {
				const fileUploader = document.createElement("input");
				fileUploader.setAttribute("type", "file");
				fileUploader.style.display = "none";
				document.body.appendChild(fileUploader);
				fileUploader.click();
				fileUploader.addEventListener("change", () => {
					const storageRef = firebase.storage().ref();
					const url = `upload/${Math.random()
						.toString(36)
						.slice(2)}.jpg`;
					const ref = storageRef.child(url);
					this.options[0] = "Uploading image...";
					ref.put(fileUploader.files[0]).then(snapshot => {
						database.ref(`/conversation`).update({
							imageUrl: url
						});
						this.currentQ = "image_upload";
						setTimeout(() => {
							fileUploader.parentNode.removeChild(fileUploader);
							this.sendMessage(`IMAGE_URL|${url}`);
						}, 10);
					});
				});
				return;
			}
			let animator = document.createElement("div");
			animator.innerHTML = text;
			animator.classList.add("animator");
			document.body.appendChild(animator);
			this.messages.push({
				sender: "sender-2",
				text: text,
				class: "temp",
				avatar: "/user.png",
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			setTimeout(() => {
				const elements = document.querySelectorAll(".options li button");
				document.querySelector(".options ul").style.opacity = "0";
				document.querySelector(".options ul").addEventListener("transitionend", () => {
					document.querySelector(".options ul").style.display = "none";
				});
				elements.forEach(element => {
					if (element.innerText === text) {
						element.style.visibility = "hidden";
						const bound = getOffset(element);
						animator.style.width = `${element.offsetWidth + 1}px`;
						animator.style.top = `${bound.top}px`;
						animator.style.opacity = "1";
						animator.style.left = `${bound.left}px`;
					}
				});
			}, 1);
			setTimeout(() => {
				let element = document.querySelector(".class-temp .message-inner");
				element.parentNode.parentNode.querySelector(
					".class-temp .sender img"
				).style.opacity =
					"1";
				const bound = getOffset(element);
				animator.style.transition = `1s`;
				animator.style.top = `${bound.top - this.$el.querySelector("main").scrollTop}px`;
				animator.style.left = `${bound.left}px`;
				animator.addEventListener("transitionend", () => {
					try {
						animator.parentNode.removeChild(animator);
						this.messages.pop();
						this.sendMessage(text);
					} catch (e) {}
					return;
				});
			}, 10);
		},
		startSpeech() {
			if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
				this.speaking = true;
				const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
				recognition.start();
				recognition.addEventListener("result", text => {
					recognition.stop();
					this.sendMessage(sentenceCase(text.results[0][0].transcript));
					this.speaking = false;
				});
			}
		},
		respond(text) {
			this.options = [];
			let currentTime = new Date().getTime();
			return new Promise((resolve, reject) => {});
		},
		botSays(text, options = []) {
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-1";
			}
			if ("speechSynthesis" in window) {
				let voices = window.speechSynthesis.getVoices();
				const utterThis = new SpeechSynthesisUtterance(
					text.replace(
						/([\uE000-\uF8FF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDDFF])/g,
						""
					)
				);
				// utterThis.rate = 1.25;
				let a = setInterval(() => {
					voices = window.speechSynthesis.getVoices();
					voices.forEach(voice => {
						if (voice.name === "Google US English") {
							utterThis.voice = voice;
						}
					});
					if (voices.length > 0) {
						clearInterval(a);
						// window.speechSynthesis.speak(utterThis);
					}
				}, 10);
				setTimeout(() => {
					clearInterval(a);
				}, 2000);
			}
			const message = {
				sender: "sender-1",
				text: text,
				avatar: this.currentImage,
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			};
			if (options) {
				message.options = options;
				this.options = options;
			}
			this.messages.push(message);
			this.saveMessages();
		},
		sendMessage(reply = this.reply) {
			if (typeof reply !== "string") reply = this.reply;
			this.reply = "";
			if (!reply || !reply.trim()) return;
			if (reply.toLowerCase() === "clear") {
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
											location.reload();
										}
									}
								});
							});
					});

				location.reload();
				return;
			}
			if (this.messages.length > 0) {
				this.messages[this.messages.length - 1].next = "sender-2";
			}
			this.messages.push({
				sender: "sender-2",
				text: reply,
				avatar: "/user.png",
				previous:
					this.messages.length > 0
						? this.messages[this.messages.length - 1].sender
						: "unknown"
			});
			this.saveMessages();
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
			if (this.currentQ) {
				const updator = {};
				if (this.currentQ === "when_happened") {
					updator[this.currentQ] = chrono.parseDate(reply);
				} else {
					updator[this.currentQ] = reply;
				}
				database.ref(`/data`).update(updator);
			}
			if (!this.bossHasJoined) {
				this.respond(reply)
					.then(response => {
						this.respondResponse(response);
					})
					.catch(() => {});
			}
			fetch("https://api.dialogflow.com/v1/query", {
				method: "POST",
				headers: {
					Authorization: `Bearer df0640e456d14fb4a7c2e967e1cf7b38`,
					"content-type": "application/json; charset=utf-8"
				},
				body: JSON.stringify({
					query: reply,
					contexts: this.contexts,
					lang: "en",
					sessionId: Math.random()
						.toString(36)
						.slice(2)
				})
			})
				.then(response => response.json())
				.then(json => {
					try {
						const answer = json.result.speech;
						this.botSays(answer || "😊");
						if (
							answer ===
							"Okay, I have unlocked the door. Do you want me to to add to your trusted list?"
						) {
							this.contexts = ["door-unlock-followup"];
							firebase
								.database()
								.ref(`/`)
								.update({
									access: true
								});
							setTimeout(() => {
								firebase
									.database()
									.ref(`/`)
									.update({
										access: false
									});
							}, 10000);
						} else if (
							answer === "Okay, great. I'll let them in next time. What's their name?"
						) {
							this.contexts = ["door-unlock-yes-followup"];
						} else if (answer === "Here's the list of people.") {
							this.$router.push("/people");
						} else if (this.contexts[0] === "door-unlock-yes-followup") {
							const name = json.result.resolvedQuery;
							console.log(lastImage);
							if (lastImage) {
								firebase
									.database()
									.ref(`/rings/${lastImage}`)
									.update({
										name: name,
										userData: "trusted"
									});
								fetch(
									"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/add-image-to-collection/final",
									{
										method: "POST",
										headers: {
											"content-type": "application/json"
										},
										body: JSON.stringify({
											url: this.people[lastImage].url,
											name: name,
											userData: "trusted"
										})
									}
								).then(() => {
									fetch(
										"https://dohdatasciencevm18.westeurope.cloudapp.azure.com/rstudio/train-collection/final"
									);
									this.botSays("Done!");
								});
							}
						}
					} catch (error) {}
				})
				.catch(error => {});
		},
		respondResponse(response) {
			this.botSays(response.text, response.options);
			setTimeout(() => {
				this.$el.querySelector("main").scrollTop = this.$el.querySelector(
					"main"
				).scrollHeight;
			}, 1);
			let l = this.nextMessages.length;
			let count = 0;
			let x = setInterval(() => {
				this.typing = false;
				if (count === l) {
					this.nextMessages = [];
					clearInterval(x);
					return;
				}
				this.botSays(this.nextMessages[count].text, this.nextMessages[count].options);
				setTimeout(() => {
					this.$el.querySelector("main").scrollTop = this.$el.querySelector(
						"main"
					).scrollHeight;
				}, 1);
				count++;
			}, 1);
		}
	}
};
</script>

<style lang="scss" scoped>
main {
	padding: 1.5rem;
}
.message-block {
	.message-content {
		display: flex;
		justify-content: flex-start;
	}
	.message {
		flex: 1 0 0;
		.message-inner {
			background-color: #ffffff;
			display: inline-block;
			padding: 0.75rem 1rem;
			box-shadow: 0 0.5rem 1rem rgba(0, 100, 100, 0.1);
			border-radius: 25px;
		}
		.emoji {
			font-size: 50%;
			display: inline-block;
			margin-left: 0.65rem;
			transform: scale(2) translateY(-0.075rem);
		}
	}
	.sender {
		margin-right: 0.5rem;
		width: 25px;
		img {
			width: 25px;
			height: 25px;
			border-radius: 15px;
		}
	}
	&.sender-2 {
		.message-inner {
			background-color: #5352ed;
			color: #fff;
		}
	}
	&.sender-1 + .sender-2,
	&.sender-1 + .sender-3,
	&.sender-2 + .sender-1,
	&.sender-2 + .sender-3,
	&.sender-3 + .sender-1,
	&.sender-3 + .sender-2 {
		margin-top: 1.5rem;
	}
	&.sender-3 + .sender-3 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-2 + .sender-2 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-1 + .sender-1 {
		margin-top: 0.25rem;
		.sender img {
			visibility: hidden;
		}
	}
	&.sender-2 {
		.message {
			display: flex;
			justify-content: flex-end;
		}
		.sender {
			margin-right: 0;
			margin-left: 0.5rem;
		}
	}
	&.sender-1.next-sender-1,
	&.sender-3.next-sender-3 {
		.message-inner {
			border-bottom-left-radius: 15px;
		}
		+ div {
			.message-inner {
				border-top-left-radius: 15px;
			}
		}
	}
	&.sender-2.next-sender-2 {
		.message-inner {
			border-bottom-right-radius: 15px;
		}
		+ div {
			.message-inner {
				border-top-right-radius: 15px;
			}
		}
	}
	&.sender-1.next-sender-1.previous-sender-1,
	&.sender-3.next-sender-3.previous-sender-3,
	&.sender-2.next-sender-2.previous-sender-2 {
		.message-inner {
			border-top-right-radius: 15px;
			border-bottom-right-radius: 15px;
		}
	}
	&.typing {
		.ellipsis-1 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 0;
		}
		.ellipsis-2 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 333ms;
		}
		.ellipsis-3 {
			display: inline-block;
			animation: pulse 1s infinite;
			animation-delay: 666ms;
		}
	}
	&.meta {
		font-size: 85%;
		margin: 1.5rem 0;
		text-align: center;
		opacity: 0.75;
	}
}
.agastya--night .message .message-inner {
	background-color: #000;
	box-shadow: 0 0.5rem 1rem rgba(255, 255, 255, 0.2);
}
@keyframes pulse {
	0% {
		transform: translateY(0);
		opacity: 1;
	}
	50% {
		opacity: 0.25;
		transform: translateY(-5px);
	}
	100% {
		transform: translateY(0);
		opacity: 1;
	}
}
footer {
	z-index: 1000;
}
button,
select,
input {
	background: none;
	font: inherit;
}
.reply-box {
	box-shadow: 0 -0.5rem 1rem rgba(0, 100, 100, 0.05);
	form {
		display: flex;
		justify-content: space-between;
	}
	input,
	button {
		border: none;
		padding: 1rem;
	}
	button {
		i {
			color: #5352ed;
			transform: scale(1.5);
		}
	}
	input {
		width: 100%;
	}
}
.options {
	position: relative;
	&::before {
		content: "";
		position: absolute;
		left: 0;
		right: 0;
		height: 2rem;
		top: -2rem;
		background: linear-gradient(transparent, #f3f6f7);
	}
	background: #f3f6f7;
	ul {
		transition: 500ms;
		margin: 0;
		padding: 0;
		list-style: none;
		white-space: nowrap;
		width: 100%;
		overflow-x: auto;
		li {
			display: inline-block;
			margin: 0;
			padding: 5px 0 1rem 1rem;
			&:last-of-type {
				padding-right: 1rem;
			}
			button {
				background-color: #5352ed;
				color: #fff;
				border: none;
				padding: 0.75rem 1rem;
				border-radius: 25px;
			}
		}
	}
}
.class-temp {
	.message {
		visibility: hidden;
	}
	.sender img {
		opacity: 0;
		transition: 500ms;
	}
}
input {
	outline: none;
}
.inline-image {
	overflow: hidden;
	img {
		margin: -1rem;
		width: calc(100% + 2rem);
		max-width: calc(100% + 2rem);
	}
}
.has-attachment {
	background-color: #34495e;
	color: rgba(255, 255, 255, 0.75);
	padding: 1rem;
	margin: 0.25rem 0;
	border-radius: 15px;
	:first-child {
		text-align: center;
		color: #fff;
	}
}
header {
	padding: 1rem 0 0.5rem 0;
	img {
		height: 25px;
	}
}
</style>
