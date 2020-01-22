<template>
  <div class="modal" :class="{ 'is-active' : view  }">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <div class="card" v-if="view">
        <div class="card-content">
          <p class="title">Import Contact</p>
          <br />
          <p>
            Please follow the below format to import data in
            <span class="tag is-info">csv</span> format.
            <br />Leave blank if data not required
          </p>
          <hr />
          <table class="table is-bordered is-narrow">
            <thead>
              <th>Company Name</th>
              <th>Contact Person</th>
              <th>Address</th>
              <th>City</th>
              <th>State</th>
              <th>Country</th>
              <th>Ph #1</th>
              <th>Ph #2</th>
              <th>Email</th>
            </thead>
            <tbody>
              <tr>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
                <td>...</td>
              </tr>
            </tbody>
          </table>
          <br />
          <div class="field">
            <div class="control">
              <label class="label">Tag your Contacts</label>

              <b-taginput
                v-model="form.tags"
                :data="data_tag"
                autocomplete
                field="name"
                placeholder="Add a tag"
                @typing="getTag"
              >
                <template slot-scope="props">{{props.option.name}}</template>
                <template slot="header">
                  <a @click="showAddData('tag')">
                    <span>Add new...</span>
                  </a>
                </template>
              </b-taginput>
            </div>
          </div>
          <br>
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
                <span class="file-label">Upload file</span>
              </span>
              <span class="file-name" v-html="filename"></span>
            </label>
          </div>
        </div>
        <footer class="card-footer">
          <a class="card-footer-item has-text-info" @click="submit">
            <span class="icon icon-btn">
              <feather type="check" size="1.3rem"></feather>
            </span>
            Save
          </a>
          <p class="card-footer-item">
            <span class="icon icon-btn">
              <feather type="x" size="1.3rem"></feather>
            </span>
            Close
          </p>
        </footer>
      </div>
    </div>
    <div class="modal-close"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    view: { type: Boolean, default: false }
  },
  data() {
    return {
      form: {
        file: null,
        tags: [],

      },
    filename: "data.csv",
      data_tag: [],
      tagList: [],

      query_tag: ""
    };
  },
  mounted() {
    let self = this;
    this.$axios
      .get("/get/tag")
      .then(function(response) {
        console.log(response);
        self.data_tag = response.data;
        self.tagList = response.data;
      })
      .catch(function(error) {
        console.log(error);
        self.$buefy.snackbar.open({
          duration: 4000,
          message: "Unable to fetch data for Tags",
          type: "is-light",
          position: "is-top-right",
          actionText: "Close",
          queue: true,
          onAction: () => {
            self.isActive = false;
          }
        });
      });
  },
  methods: {
    getTag(text) {
      this.data_tag = this.tagList.filter(option => {
        return (
          option.name
            .toString()
            .toLowerCase()
            .indexOf(text.toLowerCase()) >= 0
        );
      });
    },

    closeModal() {
      this.form.file = null;
      this.form.filename = "data.csv";
      this.$emit("closeModal");
    },
    onSelectFile() {
      const input = this.$refs.fileInput;
      console.log(input.files);
      this.form.filename = input.files[0].name;
    },
    submit() {
      let self = this;
      let formData = new FormData();
      formData.append("file", this.form.file);
      this.$axios
        .post("/upload/contacts", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(function(response) {
          if (response.data.success) {
            self.closeModal();
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.success,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                self.isActive = false;
              }
            });
          } else {
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.data.message,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                self.isActive = false;
              }
            });
          }
        });
    }
  }
};
</script>

<style scoped>
</style>