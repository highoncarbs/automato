<template>
  <div class="modal" :class="{ 'is-active' : view}">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content">
      <div class="card">
        <div class="card-content">
          <p class="title">New Job</p>
          <br />
          <div class="field">
            <div class="control">
              <label class="label">Group</label>

              <b-taginput
                v-model="form.club"
                :data="data_club"
                autocomplete
                field="name"
                placeholder="Add a club"
                @typing="getClub"
              ></b-taginput>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <label class="label">Template</label>
              <b-autocomplete
                v-model="query_template"
                placeholder="Select"
                :keep-first="true"
                :open-on-focus="true"
                :data="autocompleteTemplate"
                field="name"
                @select="getTemplate"
              ></b-autocomplete>
              <small class="tag is-danger is-light is-underline" v-if="form.errors.template">
                Date
                Required
              </small>
            </div>
          </div>
          <label class="label">Select Job type</label>
          
          <b-field position="is-left">
            <b-radio-button v-model="form.type" native-value="whatsapp" type="is-black">
              <span>Whatsapp</span>
            </b-radio-button>

            <b-radio-button v-model="form.type" native-value="sms" type="is-black">
              <span>SMS</span>
            </b-radio-button>
          </b-field>
        </div>

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
        type: "whatsapp",
        template: null,
        club: [],
        errors: {
          template: false,
          club: false
        }
      },
      query_template: "",
      data_template: [],
      data_club: [],
      clubList: []
    };
  },
  computed: {
    autocompleteTemplate() {
      if (this.data_template.length != 0) {
        return this.data_template.filter(option => {
          return (
            option.name
              .toString()
              .toLowerCase()
              .indexOf(this.query_template.toLowerCase()) >= 0
          );
        });
      }
    }
  },
  mounted() {
    let self = this;
    this.$axios
      .get("/get/template")
      .then(function(response) {
        console.log(response.data);
        self.data_template = response.data;
      })
      .catch(function(error) {
        console.log(error);
        self.$buefy.snackbar.open({
          duration: 4000,
          message: "Unable to fetch data for Template",
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
      .get("/get/club")
      .then(function(response) {
        self.data_club = response.data;
        self.clubList = response.data;
      })
      .catch(function(error) {
        console.log(error);
        self.$buefy.snackbar.open({
          duration: 4000,
          message: "Unable to fetch data for Club",
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
    getTemplate(option) {
      if (option != null) {
        this.form.template = option.id;
      } else {
        this.form.template = null;
      }
    },
    getClub(text) {
      this.data_club = this.clubList.filter(option => {
        return (
          option.name
            .toString()
            .toLowerCase()
            .indexOf(text.toLowerCase()) >= 0
        );
      });
    },
    submit() {
      let self = this;

      this.$axios.post("/add/job", self.form).then(function(response) {
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