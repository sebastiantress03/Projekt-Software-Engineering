<script setup>
	import axios from 'axios'
	import Ergebnis from "@/components/Ergebnis.vue"
	import { ref } from 'vue'
	
	let ergebnisse = ref([]);


	// Aktuallisierung für neue Schnittstelle /tournaments/{matchplan}
	function getData(){
		new Promise((resolve,reject) => {
			axios.get("http://127.0.0.1:8000/").then(
				response => {
					if(response.data.data) {
						
					
						let ergebnisseDictionary = {};
						response.data.data.forEach(element => {
							ergebnisseDictionary[element[0]] = { "actual" : element, "copy" : element };
						});
						localStorage.setItem("ergebnisse",JSON.stringify(ergebnisseDictionary))
						ergebnisse.value = response.data.data;
						resolve();
					}
				}
			).catch(err => {
				ergebnisse.value = []
				let storage = JSON.parse(localStorage.getItem("ergebnisse"));
				for(const key in storage) {
					ergebnisse.value.push(storage[key]["actual"])
				}
				resolve();
			});
	
		});
		
	}

	function saveChanges(){
		let storage = JSON.parse(localStorage.getItem("ergebnisse"));
		for (const key in storage) {

			if((storage[key]["actual"][3] != storage[key]["copy"][3]) || (storage[key]["actual"][4] != storage[key]["copy"][4]) )
			axios.put("http://127.0.0.1:8000/scores/"+key,{"spielergebnis1":storage[key]["actual"][3],"spielergebnis2":storage[key]["actual"][4]}).then(
				response => {
					if (response.data.status_code == 200) {
						storage[key]["copy"] = storage[key]["actual"];
					}
				}
			);
		}
		localStorage.setItem("ergebnisse",JSON.stringify(storage));
	}

</script>

<template>
	<div id="wrapper">
		<button @click="getData()">Aktuelle Spielstände</button>
		<div id="Ergebnistabelle"> 
			<Ergebnis v-for="table in ergebnisse"
					 :spielID=table[0]
					 :teamID1=table[1]
					 :teamID2=table[2]
					 :spielergebnis1=table[3]
					 :spielergebnis2=table[4]
					 :hinrückspiel=table[5] />
		</div>	
	</div> 
	<button @click="saveChanges()" class="saveChange">
		Speichern
	</button>
</template>

<style scoped>
	#wrapper {
		display: flex;
		color: black;
		flex-direction: column;
		justify-content: center;
		margin: 25px;
		align-items: center;
	}

</style>
