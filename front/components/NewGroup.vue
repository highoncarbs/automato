<template>
  <div class="modal" :class="{ 'is-active' : view}">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-content is-fullwidth is-expanded">
      <div class="card">
        <div class="card-content">
          <p class="title">New Group</p>

          <p class="subtitle is-size-6 has-text-grey">
            Select either the
            <b>Contacts</b> or
            <b>Tags & Location</b>
          </p>
          <label for class="label">Group Name</label>
          <input type="text" placeholder="Enter Group Name" v-model="form.name" class="input" />
          <hr />
          <b-tabs v-model="activeTab" type="is-toggle">
            <b-tab-item label="Tags">
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
            </b-tab-item>

            <b-tab-item label="Location">
              <label class="label">City</label>
              <b-taginput
                v-model="form.city"
                :data="data_city"
                autocomplete
                field="name"
                placeholder="Add City"
                @typing="getCity"
              >
                <template slot-scope="props">{{props.option.name}}</template>
                <template slot="header">
                  <a @click="showAddData('city')">
                    <span>Add new...</span>
                  </a>
                </template>
              </b-taginput>
            </b-tab-item>

            <b-tab-item label="Contacts">
              <b-table
                :data="data"
                :loading="loading"
                paginated
                backend-pagination
                :total="total"
                :per-page="perPage"
                @page-change="onPageChange"
                aria-next-label="Next page"
                aria-previous-label="Previous page"
                aria-page-label="Page"
                aria-current-label="Current page"
                backend-sorting
                :default-sort-direction="defaultSortOrder"
                :default-sort="[sortField, sortOrder]"
                @sort="onSort"
                :checked-rows.sync="form.contacts"
                :current-page.sync="page"
                checkable
                :checkbox-position="checkboxPosition"
              >
                <template slot-scope="props">
                  <b-table-column field="name" label="Name" sortable>{{ props.row.name }}</b-table-column>

                  <b-table-column field="city" label="City">{{ props.row.city[0].name }}</b-table-column>
                </template>
              </b-table>
            </b-tab-item>
          </b-tabs>
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
      activeTab: 0,
      form: {
        name: null,
        city: [],
        tags: [],
        contacts: [],
        errors: {
          city: false,
          tag: false
        }
      },
      checkboxPosition: "left",
      data_city: [],
      cityList: [],
      data_tag: [],
      tagList: [],
      data: [],
      total: 0,
      loading: false,
      sortField: "name",
      sortOrder: "desc",
      defaultSortOrder: "desc",
      page: 1,
      perPage: 20
    };
  },

  mounted() {
    this.loadAsyncData();
    let self = this;
    this.$axios
      .get("/get/city")
      .then(function(response) {
        console.log(response.data);
        self.data_city = response.data;
        self.cityList = response.data;
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
    loadAsyncData() {
      let self = this;
      const params = {
        sort_by: this.sortField,
        sort_order: this.sortOrder,
        page: this.page
      };

      this.loading = true;
      this.$axios
        .$post("/get/contacts", params)
        .then(function(response) {
          self.data = response;
          // let currentTotal = data.total_results
          // if (data.total_results / this.perPage > 1000) {
          //     currentTotal = this.perPage * 1000
          // }
          // this.total = currentTotal
          // data.results.forEach((item) => {
          //     item.release_date = item.release_date.replace(/-/g, '/')
          //     this.data.push(item)
          // })
          self.loading = false;
        })
        .catch(error => {
          this.data = [];
          this.total = 0;
          this.loading = false;
          throw error;
        });
    },
    onPageChange(page) {
      this.page = page;
      this.loadAsyncData();
    },
    onSort(field, order) {
      this.sortField = field;
      this.sortOrder = order;
      this.loadAsyncData();
    },
    closeModal() {
      this.$emit("closeModal");
    },
    getCity(text) {
      this.data_city = this.cityList.filter(option => {
        return (
          option.name
            .toString()
            .toLowerCase()
            .indexOf(text.toLowerCase()) >= 0
        );
      });
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

      this.$axios.post("/add/club", self.form).then(function(response) {
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