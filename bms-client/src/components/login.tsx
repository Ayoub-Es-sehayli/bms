import {
    Anchor,
    Button,
    Center,
    Checkbox,
    Container,
    Group,
    Paper,
    PasswordInput,
    Stack,
    TextInput,
    Title,
} from '@mantine/core';
import { useForm } from '@tanstack/react-form';
import { Link } from '@tanstack/react-router';
import { z } from "zod"

const FormSchema = z.object({
    email: z.string({ required_error: "An email address is required" }).email("Must enter a valid email address"),
    password: z.string({ required_error: "A password is required" }).min(8, "A password needs to be at least 8 characters long"),
    rememberMe: z.boolean()
})
type FormType = z.infer<typeof FormSchema>

export type Props = {
    onSubmit: (credentials: FormType) => void
}

function LoginForm({ onSubmit }: Props) {
    const form = useForm<FormType>({
        defaultValues: {
            email: "",
            password: "",
            rememberMe: false
        },
        onSubmit: async ({ value }) => {
            console.log(value)
            onSubmit(value)
        },
        validators: {
            onBlurAsync: FormSchema,
            onSubmitAsync: FormSchema
        }
    })
    const handleSubmit = (e) => {
        e.preventDefault()
        e.stopPropagation()
        form.handleSubmit()
    }
    return (
        <Center>
            <Container miw="33%">
                <Title ta="center">
                    Welcome!
                </Title>

                <Paper withBorder shadow="md" radius="md" component='form' onSubmit={handleSubmit}>
                    <Stack gap="md" p="lg">
                        <form.Field
                            name='email'
                            children={(field) => (
                                <TextInput name={field.name}
                                    value={field.state.value}
                                    onBlur={field.handleBlur}
                                    onChange={(e) => field.handleChange(e.target.value)}
                                    error={field.state.meta.errors.length > 0 ? field.state.meta.errors : false}
                                    label="Email"
                                    placeholder="you@bms.com"
                                    required />
                            )}
                        />
                        <form.Field
                            name='password'
                            children={(field) => (
                                <PasswordInput name={field.name}
                                    value={field.state.value}
                                    onBlur={field.handleBlur}
                                    onChange={(e) => field.handleChange(e.target.value)}
                                    error={field.state.meta.errors.length > 0 ? field.state.meta.errors : false}
                                    label="Password"
                                    placeholder='Your password'
                                    required />
                            )}
                        />
                        <Group justify='space-between'>
                            <form.Field
                                name="rememberMe"
                                children={(field) => (
                                    <Checkbox name={field.name}
                                        checked={field.state.value}
                                        onChange={(e) => field.handleChange(e.target.checked)}
                                        onBlur={field.handleBlur}
                                        label="Remember me" />
                                )}
                            />
                            <Anchor component={Link} size="sm">Forget password?</Anchor>
                        </Group>
                        <Button type='submit'>Sign In</Button>
                    </Stack>
                </Paper>
            </Container>
        </Center>
    )
}

export default LoginForm
