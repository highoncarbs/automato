<template>
  <div class="modal" :class="{ 'is-active' : view  }">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <div class="card" v-if="view">
        <div class="card-content">
          <p class="title">New Contact</p>
          <br />
          <div class="field">
            <div class="control">
              <label for class="label">Name</label>
              <input
                type="text"
                placeholder="Enter Business Name"
                v-model="form.name"
                class="input"
              />
            </div>
          </div>
          <div class="field-body is-grouped is-multiline">
            <div class="field">
              <div class="control">
                <label for class="label">Contact #1</label>
                <input
                  type="text"
                  placeholder="Enter Contact Number"
                  v-model="form.contact_one"
                  class="input"
                />
              </div>
            </div>
            <div class="field">
              <div class="control">
                <label for class="label">Contact #2</label>
                <input
                  type="text"
                  placeholder="Enter Contact Number"
                  v-model="form.contact_two"
                  class="input"
                />
              </div>
            </div>
          </div>
          <div class="field-body is-grouped is-multiline" style="margin: 0.5rem 0 0.5rem 0">
            <div class="field">
              <div class="control">
                <label class="label">City</label>
                <b-autocomplete
                  v-model="query_city"
                  placeholder="Select"
                  :keep-first="true"
                  :open-on-focus="true"
                  :data="autocompleteCity"
                  field="name"
                  @select="getCity"
                >
                  <template slot="header">
                    <a @click="showAddData('city')">
                      <span>Add new...</span>
                    </a>
                  </template>
                  <template slot="empty">No results for {{ query_city }}</template>
                </b-autocomplete>
                <small class="tag is-danger is-light is-underline" v-if="form.errors.city">
                  Date
                  Required
                </small>
              </div>
            </div>
            <div class="field">
              <div class="control">
                <label for class="label">Email</label>
                <input type="email" placeholder="Enter Email" v-model="form.email" class="input" />
              </div>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="label">Tags</label>

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
          <div class="field">
            <div class="control">
              <label for class="label">Address</label>
              <textarea
                type="text"
                placeholder="Enter Address"
                v-model="form.address"
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
    view: { type: Boolean, default: false },
  },
  data() {
    return {
      form: {
        name: null,
        contact_one: null,
        contact_two: "",
        email: "",
        address: "",
        city: null,
        tags: [],
        errors: {
          name: false,
          contact_one: false,
          city: false
        }
      },

      data_city: [],
      data_tag: [],
      tagList: [],
      query_city: "",
      query_tag: ""
    };
  },
  mounted() {
    let self = this;
    this.$axios
      .get("/get/city")
      .then(function(response) {
        console.log(response.data);
        self.data_city = response.data;
      })
      .catch(function(error) {
        console.log(error);
        self.$buefy.snackbar.open({
          duration: 4000,
          message: "Unable to fetch data for City",
          type: "is-light",
          position: "is-top-right",
          actionText: "Close",
          queue: true,
          onAction: () => {
            self.isActive = false;
          }
        });
      });
    this.$axios
      .get("/get/tag")
      .then(function(response) {
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
 
  computed: {
    autocompleteCity() {
      if (this.data_city.length != 0) {
        return this.data_city.filter(option => {
          return (
            option.name
              .toString()
              .toLowerCase()
              .indexOf(this.query_city.toLowerCase()) >= 0
          );
        });
      }
    }
  },
  methods: {
    getCity(option) {
      if (option != null) {
        this.form.city = option.id;
      } else {
        this.form.city = null;
      }
    },
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

    setCity(option) {
      if (option != null) {
        this.query_city = option.name;
      } else {
      }
    },
    showAddData(val) {
      let self = this;
      this.$buefy.dialog.prompt({
        message: `<b>Add Data</b> `,
        inputAttrs: {
          placeholder: "e.g. Data",
          maxlength: 100,
          value: this.name
        },
        confirmText: "Add",
        onConfirm: value => {
          let formdata = { name: value };
          this.$axios
            .post("/add/" + String(val), formdata)
            .then(function(response) {
              console.log(response.data);
              if (response.data.success) {
                switch (val) {
                  case "city":
                    self.data_city.push(response.data.data);
                    break;
                  case "tag":
                    self.tagList.push(response.data.data);
                    break;
                  default:
                    break;
                }
                self.$buefy.snackbar.open({
                  duration: 4000,
                  message: response.data.success,
                  type: "is-light",
                  position: "is-top-right",
                  actionText: "Close",
                  queue: true,
                  onAction: () => {
                    this.isActive = false;
                  }
                });
              } else {
                if (response.data.message) {
                  self.$buefy.snackbar.open({
                    duration: 4000,
                    message: response.data.message,
                    type: "is-light",
                    position: "is-top-right",
                    actionText: "Close",
                    queue: true,
                    onAction: () => {
                      this.isActive = false;
                    }
                  });
                }
              }
            })
            .catch(function(error) {
              console.log(error);
            });
        }
      });
    },
    closeModal() {
      this.data = [];
      this.$emit("closeModal");
    },
    submit() {
      let self = this;

      this.$axios.post("/add/contacts", self.form).then(function(response) {
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