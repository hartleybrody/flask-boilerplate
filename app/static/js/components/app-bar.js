export default {
    props: {
        'is_logged_in': Boolean
    },
    data() {
        let nav_items = []
        if (this.is_logged_in){
            nav_items = [
                {name: "Dash", url: "/dash/"},
                {name: "Logout", url: "/logout/"},
            ]
        } else {
            nav_items = [
                {name: "Login", url: "/login/"},
                {name: "Sign Up", url: "/sign-up/"},
            ]
        }
        return {
            nav_items: nav_items,
            drawer: false,
        }
    },
    template: `
        <v-sheet>
            <v-app-bar
                dense
                dark
            >
                <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>

                <v-toolbar-title>{{APP_NAME}}</v-toolbar-title>

                <v-spacer></v-spacer>

                <v-btn icon>
                    <v-icon>mdi-heart</v-icon>
                </v-btn>

            </v-app-bar>

            <v-navigation-drawer
                v-model="drawer"
                absolute
                temporary
            >
                <v-list
                    nav
                    dense
                >
                    <v-list-item-group>
                        <v-list-item v-for="item in this.nav_items" v-bind:key="item.url">
                            <v-list-item-icon>
                                <v-icon>{{item.icon}}</v-icon>
                            </v-list-item-icon>
                            <v-list-item-title>{{item.name}}</v-list-item-title>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
            </v-navigation-drawer>
        </v-sheet>

        `
}
