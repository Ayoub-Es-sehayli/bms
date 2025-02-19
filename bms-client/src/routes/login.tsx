import { createFileRoute } from "@tanstack/react-router";
import LoginForm, { Props as FormProps } from "../components/login";

export const Route = createFileRoute("/login")({
    component: LoginPage
})

function LoginPage() {
    const loginFn: FormProps['onSubmit'] = (credentials) => {
        console.log(credentials)
    }
    return <LoginForm onSubmit={loginFn} />
}
