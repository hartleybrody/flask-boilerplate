export default {
    props: ['session_type'],
    data() {
        let nav_items = []
        if (this.session_type == "anonymous"){
            nav_items = "anon"
        } else {
            nav_items = "user"
        }
        return {
            nav_items: nav_items
        }
    },
    template: `
        <v-app-bar
            dense
            dark
        >
            <v-app-bar-nav-icon></v-app-bar-nav-icon>

            <v-toolbar-title>{{APP_NAME}} + {{nav_items}}</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn icon>
                <v-icon>mdi-heart</v-icon>
            </v-btn>

        </v-app-bar>`
}
