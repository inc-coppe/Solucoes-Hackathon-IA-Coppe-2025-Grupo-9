import { Home, ClipboardList, FileCheck, History, Settings, LogOut, User, Bell } from "lucide-react";
import { NavLink } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
  SidebarHeader,
  useSidebar,
} from "@/components/ui/sidebar";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

const items = [
  { title: "INÍCIO", url: "/", icon: Home },
  { title: "VALIDAÇÃO", url: "/validacao", icon: FileCheck },
  { title: "SOLICITAÇÃO", url: "/regulacoes", icon: ClipboardList },
  { title: "ESCALAS", url: "/historico", icon: History },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="border-b border-sidebar-border py-4 px-3">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10 bg-accent">
            <AvatarFallback className="bg-accent text-accent-foreground">
              <User className="h-5 w-5" />
            </AvatarFallback>
          </Avatar>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-sidebar-foreground truncate">
                Olá, <span className="text-accent">Juliana</span>!
              </p>
              <p className="text-xs text-sidebar-foreground/70 truncate">
                SMS - Gestor Municipal
              </p>
              <button className="text-xs text-accent hover:underline mt-0.5">
                Acessar Perfil
              </button>
            </div>
          )}
        </div>
        {!collapsed && (
          <Button
            variant="ghost"
            size="sm"
            className="w-full justify-start gap-2 mt-3 text-sidebar-foreground hover:bg-sidebar-accent"
          >
            <Bell className="h-4 w-4" />
            Avisos
          </Button>
        )}
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild tooltip={item.title}>
                    <NavLink
                      to={item.url}
                      end
                      className={({ isActive }) =>
                        isActive
                          ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                          : "hover:bg-sidebar-accent/50"
                      }
                    >
                      <item.icon className="h-4 w-4" />
                      <span className="text-xs font-medium">{item.title}</span>
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t border-sidebar-border">
        <div className="p-3">
          <Button
            variant="ghost"
            size="sm"
            className="w-full justify-start gap-2 text-sidebar-foreground hover:bg-sidebar-accent text-xs"
          >
            <LogOut className="h-4 w-4" />
            {!collapsed && <span>SAIR</span>}
          </Button>
          {!collapsed && (
            <div className="mt-4 text-xs text-sidebar-foreground/60 space-y-1">
              <p>Contato email@email.com.br</p>
              <p>Termos de Uso e Privacidade</p>
            </div>
          )}
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
