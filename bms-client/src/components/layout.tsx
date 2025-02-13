import {
  ActionIcon,
  Anchor,
  AppShell,
  Burger,
  Button,
  Group,
  Tooltip,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, useMatchRoute } from "@tanstack/react-router";
import { IconHome2 } from "@tabler/icons-react";
import { Route as HomeRoute } from "../routes/index";
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
      <AppShell.Navbar>
        <NavMenu />
      </AppShell.Navbar>
      <AppShell.Main>{children}</AppShell.Main>
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
        <Button>Log in</Button>
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
    <Group p={16} display="grid">
      {links.map((link) => (
        <NavbarLink {...link} />
      ))}
    </Group>
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
    <Link to={href}>
      <Tooltip label={label} position="right" transitionProps={{ duration: 0 }}>
        <ActionIcon size="lg" aria-label={label} variant={variant}>
          <Icon />
        </ActionIcon>
      </Tooltip>
    </Link>
  );
}
