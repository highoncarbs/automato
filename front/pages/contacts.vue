<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Contacts</p>
      </div>
      <div class="level-right">
        <div class="level-item">
          <button class="button" @click="addModal = !addModal">
            <span class="icon icon-btn">
              <feather type="plus" size="1.3rem"></feather>
            </span>
            Add Contact
          </button>
        </div>
        <div class="level-item">
          <button class="button" @click="importModal = !importModal">
            <span class="icon icon-btn">
              <feather type="upload-cloud" size="1.3rem"></feather>
            </span>
            Import Data
          </button>
        </div>
      </div>
    </div>
   
    <br />
    <div class="box">
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
      >
        <template slot-scope="props">
          <b-table-column field="id" label="ID" sortable width="40">{{ props.row.id }}</b-table-column>

          <b-table-column field="name" label="Name" sortable>{{ props.row.name }}</b-table-column>

          <b-table-column
            field="contact_one"
            label="Contact #1"
            sortable
          >{{ props.row.contact_one }}</b-table-column>
          <b-table-column field="city" label="City">{{ props.row.city[0].name }}</b-table-column>
          <b-table-column field="action" label="Action">
            <div class="buttons">
              <button class="button is-small" @click="addItem(props.row.id)">
                <span class="icon">
                  <feather type="user-plus" size="1rem"></feather>
                </span>
              </button>
              <button class="button is-info is-small" @click="editItem(props.row.id)">
                <span class="icon">
                  <feather type="edit" size="1rem"></feather>
                </span>
              </button>
              <button
                class="button is-danger is-small"
                @click="deleteItem(props.row.id , props.index)"
              >
                <span class="icon">
                  <feather type="x" size="1rem"></feather>
                </span>
              </button>
            </div>
          </b-table-column>
        </template>
      </b-table>
    </div>
    <NewContact :view="addModal" v-on:closeModal="addModal = !addModal" />
    <EditContact
      :view="editModal"
      :id="editDataId"
      :data="editData"
      v-on:closeModal="editModal = !editModal"
    />
    <NewImport :view="importModal" v-on:closeModal="importModal = !importModal" /> 
  </div>
</template>


<script>
import NewContact from "@/components/NewContact";
import EditContact from "@/components/EditContact";
import NewImport from "@/components/NewImport";
export default {
  components: {
    NewContact,
    EditContact,
    NewImport,
  },
  computed: {},
  mounted() {
    this.loadAsyncData();
  },
  data() {
    return {
      data: [],
      total: 5154,
      loading: false,
      sortField: "name",
      sortOrder: "desc",
      defaultSortOrder: "desc",
      page: 1,
      perPage: 20,
      addModal: false,
      editModal: false,
      importModal: false,
      editData: null,
      editDataId: null
    };
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
          let currentTotal = self.total;
          if (self.total / self.perPage > 1000) {
            let currentTotal = self.perPage * 1000;
          }
          self.total = currentTotal;

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
    type(value) {
      const number = parseFloat(value);
      if (number < 6) {
        return "is-danger";
      } else if (number >= 6 && number < 8) {
        return "is-warning";
      } else if (number >= 8) {
        return "is-success";
      }
    },
    addItem() {},
    editItem(id) {
      this.editModal = true;
      let payload = null;
      let self = this
      this.$axios.post("/get/contacts/" + String(id)).then(function(response) {
        payload = response;
        console.log(payload)
        if (payload) {
          self.editData = payload.data;
          self.editDataId = id;
        }
      });

      // this.data.filter( item =>{return item.id === id} )
    },
    deleteItem(id, index) {
      let self = this;
      this.$axios
        .$post("/delete/contacts/" + String(id))
        .then(function(response) {
          if (response.success) {
            self.data.splice(index, 1);
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.success,
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
              message: response.message,
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
  },
  filters: {
    truncate(value, length) {
      return value.length > length ? value.substr(0, length) + "..." : value;
    }
  }
};
</script>