<template>
  <div>
    <div class="hero is-fullheight">
      <div
        class="navbar is-hidden-desktop has-navbar-fixed-top has-shadow"
        style="z-index: auto !important"
      >
        <div class="container">
          <div class="navbar-brand">
            <a class="navbar-item" style="font-weight:bold;">
              <p class="is-size-4 brand-logo">automato</p>
            </a>
            <span class="navbar-burger burger" data-target="navMenu">
              <span></span>
              <span></span>
              <span></span>
            </span>
          </div>
          <div
            id="navMenu"
            class="is-hidden-dekstop navbar-menu is-shadowless has-navbar-fixed-top"
          >
            <div
              class="navbar-end is-size-5 is-center"
              style="padding-left:1rem; padding-top:2rem;"
            >
              <aside class="menu">
                <ul class="menu-list is-size-6">
                  <li>
                    <a class>
                      <span class="icon icon-btn">
                        <feather type="grid" size="1.3rem"></feather>
                      </span>
                      Dashboard
                    </a>
                  </li>
                  <li>
                    <nuxt-link to="/contacts">
                      <span class="icon icon-btn">
                        <feather type="users" size="1.3rem"></feather>
                      </span>
                      Contacts
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/groups">
                      <span class="icon icon-btn">
                        <feather type="list" size="1.3rem"></feather>
                      </span>
                      Groups
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/scrapers">
                      <span class="icon icon-btn">
                        <feather type="database" size="1.3rem"></feather>
                      </span>
                      Scrapers
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/jobs">
                      <span class="icon icon-btn">
                        <feather type="send" size="1.3rem"></feather>
                      </span>
                      Jobs
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/templates">
                      <span class="icon icon-btn">
                        <feather type="image" size="1.3rem"></feather>
                      </span>
                      Templates
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/master">
                      <span class="icon icon-btn">
                        <feather type="layers" size="1.3rem"></feather>
                      </span>
                      Master
                    </nuxt-link>
                  </li>
                  <li>
                    <nuxt-link to="/settings">
                      <span class="icon icon-btn">
                        <feather type="settings" size="1.3rem"></feather>
                      </span>
                      Settings
                    </nuxt-link>
                  </li>
                </ul>
              </aside>
            </div>
          </div>
        </div>
      </div>

      <div class="columns is-fullheight">
        <!-- Desktop nav -->
        <div class="column is-2 is-hidden-touch" id="mainmenu">
          <div id="side-menu" class="is-sidebar-menu">
            <div>
              <p class="brand-logo is-size-3">automato</p>
            </div>

            <aside class="menu" style="padding-top:5rem;">
              <ul class="menu-list is-size-6">
                <li>
                  <a class>
                    <span class="icon icon-btn">
                      <feather type="grid" size="1.3rem"></feather>
                    </span>
                    Dashboard
                  </a>
                </li>
                <li>
                  <nuxt-link to="/contacts">
                    <span class="icon icon-btn">
                      <feather type="users" size="1.3rem"></feather>
                    </span>
                    Contacts
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/groups">
                    <span class="icon icon-btn">
                      <feather type="list" size="1.3rem"></feather>
                    </span>
                    Groups
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/scrapers">
                    <span class="icon icon-btn">
                      <feather type="database" size="1.3rem"></feather>
                    </span>
                    Scrapers
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/jobs">
                    <span class="icon icon-btn">
                      <feather type="send" size="1.3rem"></feather>
                    </span>
                    Jobs
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/templates">
                    <span class="icon icon-btn">
                      <feather type="image" size="1.3rem"></feather>
                    </span>
                    Templates
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/master">
                    <span class="icon icon-btn">
                      <feather type="layers" size="1.3rem"></feather>
                    </span>
                    Master
                  </nuxt-link>
                </li>
                <li>
                  <nuxt-link to="/settings">
                    <span class="icon icon-btn">
                      <feather type="settings" size="1.3rem"></feather>
                    </span>
                    Settings
                  </nuxt-link>
                </li>
              </ul>
            </aside>
          </div>
        </div>
        <div class="column">
          <section class="section">
            <nuxt />
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<style >
.brand-logo {
  font-family: "Libre Baskerville";
  font-weight: 700;
  letter-spacing: -2px;
}

body {
  font-family: "Inter", sans-serif;
}

.is-sidebar-menu {
  padding: 2rem;
}
.menu-list > li > a {
  font-weight: 500;
}

.icon-btn {
  margin-right: 7px !important;
  margin-bottom: 1px !important;
  vertical-align: middle !important;
}

.icon-btn-in {
  padding: 2px;
}

button {
  font-family: "Inter", sans-serif;
}
</style>

<script>
import NewContact from "./../components/NewContact.vue";
export default {
  components: {
    "new-contact": NewContact
  },
  mounted() {
    var burger = document.querySelector(".burger");
    var nav = document.querySelector("#" + burger.dataset.target);
    burger.addEventListener("click", function() {
      burger.classList.toggle("is-active");
      nav.classList.toggle("is-active");
    });
  }
};
</script>