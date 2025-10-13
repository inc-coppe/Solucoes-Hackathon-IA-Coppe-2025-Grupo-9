import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BookOpen, CheckCircle, AlertCircle } from "lucide-react";

interface AIInsight {
  id: string;
  tipo: "recomendacao" | "alerta" | "informacao";
  titulo: string;
  descricao: string;
  confianca: number;
  referencia: {
    titulo: string;
    pagina: string;
    url: string;
  };
  status: "pendente" | "aprovado" | "recusado";
}

interface AIInsightCardProps {
  insight: AIInsight;
}

export function AIInsightCard({ insight }: AIInsightCardProps) {
  const typeConfig = {
    recomendacao: {
      icon: CheckCircle,
      badge: "info" as const,
      label: "Recomendação",
    },
    alerta: {
      icon: AlertCircle,
      badge: "pending" as const,
      label: "Alerta",
    },
    informacao: {
      icon: BookOpen,
      badge: "secondary" as const,
      label: "Informação",
    },
  };

  const config = typeConfig[insight.tipo];
  const IconComponent = config.icon;

  return (
    <Card className="p-5 space-y-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-3 flex-1">
          <div className="mt-1">
            <IconComponent className="h-5 w-5 text-primary" />
          </div>
          <div className="space-y-2 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <Badge variant={config.badge}>{config.label}</Badge>
              <Badge variant="outline" className="text-xs">
                Confiança: {insight.confianca}%
              </Badge>
            </div>
            <h3 className="font-semibold text-foreground">{insight.titulo}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{insight.descricao}</p>
          </div>
        </div>
      </div>

      <div className="bg-muted/30 p-3 rounded-md border-l-4 border-primary">
        <div className="flex items-start gap-2">
          <BookOpen className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
          <div className="space-y-1">
            <p className="text-xs font-semibold text-foreground">Referência Bibliográfica</p>
            <p className="text-sm text-foreground">{insight.referencia.titulo}</p>
            <p className="text-xs text-muted-foreground">Página {insight.referencia.pagina}</p>
            <a
              href={insight.referencia.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-primary hover:underline inline-flex items-center gap-1"
            >
              Consultar documento →
            </a>
          </div>
        </div>
      </div>
    </Card>
  );
}
