<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Templates</p>
      </div>
      <div class="level-right">
        <button class="button level-item" @click="addModal = !addModal">
          <span class="icon icon-btn">
            <feather type="plus" size="1.3rem"></feather>
          </span>
          Add Template
        </button>
        <button class="button level-item" @click="getData">
          <span class="icon icon-btn">
            <feather type="refresh-cw" size="1.3rem"></feather>
          </span>
          Refresh
        </button>
      </div>
    </div>

    <br />
    <div class="columns is-multiline" v-on:closeModal="getData">
      <div class="column is-3" v-for="(item,index) in data" :key="item.id" >
        <div class="card">
          <div class="card-image" v-if='item.path != "" '>
            <figure class="image is-4by3">
              <img :src="getStatic(item.path)" alt="Placeholder image" />
            </figure>
          </div>
          <div class="card-content">
            <div class="level">
              <div class="level-left">
                <p class="title is-size-5">{{ item.name}}</p>
              </div>
              <div class="level-right">
                <span class="icon has-text-grey-light">
                  <feather type="image" v-if="item.filetype== 'image'"></feather>
                </span>
              </div>
            </div>
            <p>{{ item.message }}</p>
          </div>
          <div class="card-footer">
            <a class="card-footer-item" @click="editItem(item.id)">
              <span class="icon icon-btn">
                <feather type="edit" size="1.3rem" />
              </span>
              Edit
            </a>
            <a class="card-footer-item has-text-danger" @click="deleteItem(index ,item.id)">
              <span class="icon icon-btn">
                <feather type="trash" size="1.3rem" />
              </span>
              Delete
            </a>
          </div>
        </div>
      </div>
    </div>
    <NewTemplate :view="addModal" v-on:closeModal="addModal = !addModal" />
  </div>
</template>


<script>
import axios from 'axios'
import NewTemplate from "@/components/NewTemplate"
    export default {
      components:{
       NewTemplate
      },
      computed :{

      },
      data() {
            return {
              addModal : false ,
              data: null
            }
      },  
      mounted(){
        this.getData()
  },
  methods:{
    getData(){

      let self = this 
      this.$axios.get("/get/template")
      .then(function(response){
        self.data = response.data
      })
    },
     getStatic(path) {
            if (path != "") {
                let fileSrc =String(path).split('\static')[1]
                return fileSrc
            }
            else {
                return null
            }
        },
      deleteItem(index , id){
        let self = this
        this.$axios.post( '/delete/template/'+String(id))
        .then(function(response){
          if(response.data.success){
            self.data.splice(index, 1)
          }
        })
      }
  }
    }    
</script>