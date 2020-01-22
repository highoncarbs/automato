<template>
  <div class="modal" :class="{ 'is-active' : view}">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <div class="card">
        <div class="card-content">
          <p class="title">Edit Template</p>
          <br />
          <div class="field">
            <div class="control">
              <label for class="label">Name</label>
              <input
                type="text"
                v-model="form.name"
                placeholder="Enter Template Name"
                class="input"
              />
            </div>
          </div>

          <div class="file has-name is-fullwidth">
            <label class="file-label">
              <input
                class="file-input"
                @input="onSelectFile"
                ref="fileInput"
                type="file"
                name="file"
              />
              <span class="file-cta">
                <span class="file-icon">
                  <feather type="upload" size="1rem"></feather>
                </span>
                <span class="file-label">Choose a Image</span>
              </span>
              <span class="file-name">Blahblha.png</span>
            </label>
          </div>
          <br />
          <div class="field">
            <div class="control">
              <label for class="label">Enter Message</label>
              <textarea
                type="text"
                v-model="form.message"
                placeholder="Enter Message"
                class="textarea"
              />
            </div>
          </div>
        </div>
        <footer class="card-footer">
          <a class="card-footer-item has-text-info" @click="submit">
            <span class="icon icon-btn">
              <feather type="check" size="1.3rem"></feather>
            </span>
            Save
          </a>
          <p class="card-footer-item" @click="closeModal">
            <span class="icon icon-btn">
              <feather type="x" size="1.3rem"></feather>
            </span>
            Close
          </p>
        </footer>
      </div>
    </div>
    <div class="modal-close" @click="closeModal"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    view: { type: Boolean, default: false },
  },
  data(){
    return {
        form :{
            name : null ,
            message : null ,
            filetype : "image" ,
        },
        image : null ,
        
      }
  },
  watch: {
    data : function(val){
      if(Object.keys(val).length != 0){
        console.log(val)
        this.form.name= val.name
        this.form.message= val.message
        this.form.filetype= val.filetype
        this.image = val.image
     
      }
    }
  },
  methods :{
    closeModal(){
      this.$emit('closeModal')
    },
    onSelectFile() {
                const input = this.$refs.fileInput
                const files = input.files
                if (files && files[0]) {
                    const reader = new FileReader
                    reader.onload = e => {
                        this.imageData = e.target.result
                    }
                    reader.readAsDataURL(files[0])
                    this.image =  files[0]
                }
            },
    submit(){
        let self = this 
        let formData = new FormData()
        formData.append('data', JSON.stringify(this.form))
        formData.append('image', this.image)

        this.$axios.post('/add/template' ,  formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                } 
            })
        .then( function(response) {

          if(response.data.success){
            self.closeModal()
            self.$buefy.snackbar.open({
                duration: 4000,
                message: response.data.success,
                type: 'is-light',
                position: 'is-top-right',
                actionText: 'Close',
                queue: true,
                onAction: () => {
                    self.isActive = false;
                } 
            })
          }
          else{
                self.$buefy.snackbar.open({
                    duration: 4000,
                    message: response.data.message,
                    type: 'is-light',
                    position: 'is-top-right',
                    actionText: 'Close',
                    queue: true,
                    onAction: () => {
                        self.isActive = false;
                    } 
                })

          }
        })
    }
  }
}
</script>