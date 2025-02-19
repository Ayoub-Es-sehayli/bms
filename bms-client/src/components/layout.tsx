import {
    ActionIcon,
    Anchor,
    AppShell,
    Burger,
    Button,
    Group,
    Stack,
    Tooltip,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, useMatchRoute } from "@tanstack/react-router";
import { IconHome2 } from "@tabler/icons-react";
import { Route as HomeRoute } from "../routes/index";
import {Route as LoginRoute} from "../routes/login";
import React from "react";

export function LayoutComponent({ children }: React.PropsWithChildren) {
    const [opened, { toggle }] = useDisclosure();
    return (
        <AppShell
            padding="sm"
            header={{ height: 60 }}
            navbar={{ width: 66, breakpoint: "sm", collapsed: { mobile: !opened } }}
        >
            <AppShell.Header>
                <Header opened={opened} toggle={toggle} />
            </AppShell.Header>
            <AppShell.Navbar p="md">
                <NavMenu />
            </AppShell.Navbar>
            <AppShell.Main w="100vw">{children}</AppShell.Main>
        </AppShell>
    );
}

function Header({ opened, toggle }: { opened: boolean; toggle: () => void }) {
    return (
        <Group h="100%" px="md" justify="space-between">
            <Group>
                <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
                <Anchor
                    component={Link}
                    to={HomeRoute.to}
                    c="blue"
                    underline="never"
                    size="lg"
                    fw={650}
                >
                    BMS
                </Anchor>
            </Group>
            <Group>
                <Button component={Link} to={LoginRoute.to}>Log in</Button>
            </Group>
        </Group>
    );
}

function NavMenu() {
    const links: NavbarLinkProps[] = [
        {
            label: "Home",
            href: HomeRoute.to,
            icon: IconHome2,
        },
    ];
    return (
        <Stack align="center">
            {links.map((link, idx) => (
                <NavbarLink key={idx} {...link} />
            ))}
        </Stack>
    );
}

interface NavbarLinkProps {
    icon: typeof IconHome2;
    label: string;
    href: string;
}
function NavbarLink({ label, icon: Icon, href }: NavbarLinkProps) {
    const routeMatcher = useMatchRoute();
    const variant = routeMatcher({ to: href }) ? "filled" : "light";
    return (
        <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
            <ActionIcon component={Link} to={href} size="lg" aria-label={label} variant={variant}>
                <Icon />
            </ActionIcon>
        </Tooltip>
    );
}
