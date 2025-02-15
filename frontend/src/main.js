import "babel-polyfill";
import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import index from './components/index.vue'
import admin_login from './components/admin_components/admin_login.vue'
import client_login from './components/client_components/client_login.vue' 
import professional_login from './components/professional_components/professional_login.vue'
import Admin_dashboard from "./components/admin_components/admin_dashboard.vue";
import create_service from "./components/admin_components/create_service.vue";
import delete_service from "./components/admin_components/delete_service.vue";
import delete_professional from "./components/admin_components/delete_professional.vue";
import admin_clients from "./components/admin_components/admin_clients.vue";
import admin_professionals from "./components/admin_components/admin_professionals.vue";
import delete_client from "./components/admin_components/delete_client.vue";
import client_register from "./components/client_components/client_register.vue";
import client_dashboard from "./components/client_components/client_dashboard.vue";
import ClientServiceDetails from "./components/client_components/client_service_details.vue"; 
import ServiceLog from "./components/client_components/client_service_log.vue";
import professional_dashboard from "./components/professional_components/professional_dashboard.vue";
import professional_completed_services from "./components/professional_components/professional_completed_services.vue";
import professional_reviews from "./components/professional_components/professional_reviews.vue";
import professional_profile from "./components/professional_components/professional_profile.vue";
import WriteReview from './components/client_components/reviews_client.vue';
import client_signup from "./components/client_components/client_signup.vue";
import professional_signup from "./components/professional_components/professional_signup.vue";
import summary from "./components/admin_components/summary.vue";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: index
  },
  {
    path: '/admin_login',
    component: admin_login
  },
  {
    path: '/admin_dashboard',
    component: Admin_dashboard
  },
  {
    path: '/create_service',
    component: create_service
  },
  {
    path: '/delete_service',
    component: delete_service
  },
  {
    path: '/admin_professionals',
    component: admin_professionals
  },
  {
    path: '/delete_professional',
    component: delete_professional
  },
  {
    path: '/client_login',
    component: client_login
  },
  {
    path: '/professional_login',
    component: professional_login
  },
  {
    path: '/admin_clients',
    component: admin_clients
  },
  {
    path:'/ban_client',
    component: delete_client
  },
  {
    path: '/client_register',
    component: client_register
  },
  {
    path: '/client_dashboard',
    component: client_dashboard
  },
  {
    path: '/services/:service_id/professionals', // define the dynamic route path
    name: 'ServiceDetails',
    component: ClientServiceDetails, // component to render when the route is matched
    props: true, // this allows `service_id` to be passed as a prop to the component
  },
  {
    path: '/service_log',
    name: 'ServiceLog',
    component: ServiceLog, // The component that will be displayed when visiting /service_log
  },
  {
    path: '/professional_dashboard',
    component: professional_dashboard
  },
  {
    path: '/completed_services',
    component: professional_completed_services
  },
  {
    path: '/client_reviews',
    component: professional_reviews
  },
  {
    path: '/professional_profile',
    component: professional_profile
  },
  {
    path: '/write-review/:profId',
    name: 'WriteReview',
    component: WriteReview
  },
  {
    path: '/client_signup',
    component: client_signup
  },
  {
    path: '/professional_signup',
    component: professional_signup
  },
  {
    path: '/summary',
    component: summary
  }
]

const router=new VueRouter({
  routes,
  mode: 'history'

})
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
