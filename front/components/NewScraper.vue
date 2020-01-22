<template>
  <div class="modal" :class="{ 'is-active' : view}">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <div class="card">
        <div class="card-content">
          <p class="title">New Scraper</p>
          <br />
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
          <br>
          <p class="is-size-5 has-text-weight-medium">Scrape in Detail ?</p>
          <p>In detail scrapes by searching for top 100 localities in the area. 
            <br>
            Else it returns top 60 results.</p>
            <br>
           <b-field>
              <b-radio-button v-model="form.detail" native-value="Yes" type="is-black">
                <span>Yes</span>
              </b-radio-button>

              <b-radio-button v-model="form.detail" native-value="No" type="is-black">
                <span>No</span>
              </b-radio-button>
           </b-field>
        </div>
        <br />

        <footer class="card-footer">
          <a @click="submit" class="card-footer-item has-text-info">
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
export default {
  props: {
    view: { type: Boolean, default: false }
  },
  data() {
    return {
      form: {
        city: null,
        tags: [],
        detail: "Yes" ,
        errors:{
          city: false,
          tag: false,
        }
      },
      query_city: "",
      data_city: [],
      data_tag: [],
      tagList: []
    };
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
  methods: {
    closeModal() {
      this.$emit("closeModal");
    },
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
    submit() {
      let self = this;

      this.$axios.post("/add/scraper", self.form).then(function(response) {
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