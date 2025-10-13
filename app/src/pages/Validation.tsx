import { PatientCard } from "@/components/PatientCard";
import { AIInsightCard } from "@/components/AIInsightCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Brain } from "lucide-react";
import { toast } from "@/hooks/use-toast";

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

// Dados simulados
const mockPatient = {
  nome: "Maria Silva Santos",
  idade: 45,
  cpf: "123.456.789-00",
  cartaoSUS: "123 4567 8901 2345",
  dataRegulacao: "12/10/2025",
  prioridade: "alta" as const,
  especialidade: "Oftalmologia - Cirurgia de Catarata",
  cid: "H25.9",
  descricaoCid: "Catarata senil, não especificada",
  historicoClinico:
    "Paciente com diagnóstico de catarata bilateral há 2 anos. Relata diminuição progressiva da acuidade visual, principalmente para longe. Comorbidades: Diabetes Mellitus tipo 2 controlada, Hipertensão Arterial Sistêmica.",
  medicacoes: [
    "Metformina 850mg - 2x ao dia",
    "Losartana 50mg - 1x ao dia",
    "Insulina NPH - conforme orientação",
  ],
  examesRealizados: [
    "Biomicroscopia: opacificação cristaliniana bilateral",
    "Fundoscopia: sem alterações retinianas",
    "Glicemia de jejum: 110 mg/dL",
  ],
  observacoes:
    "Paciente aguarda cirurgia há 8 meses. Manifesta dificuldade para realizar atividades diárias e trabalho.",
};

const initialInsights: AIInsight[] = [
  {
    id: "1",
    tipo: "recomendacao",
    titulo: "Indicação cirúrgica compatível com protocolo",
    descricao:
      "Segundo as diretrizes do Ministério da Saúde para cirurgia de catarata, o caso apresenta critérios adequados para encaminhamento cirúrgico: acuidade visual comprometida, impacto funcional documentado e ausência de contraindicações absolutas.",
    confianca: 92,
    referencia: {
      titulo: "Portaria SAS/MS nº 957 - Protocolo Clínico de Catarata",
      pagina: "12-15",
      url: "https://bvsms.saude.gov.br/bvs/saudelegis/sas/2008/prt0957_15_12_2008.html",
    },
    status: "pendente",
  },
  {
    id: "2",
    tipo: "alerta",
    titulo: "Atenção ao controle glicêmico pré-operatório",
    descricao:
      "Paciente diabética em uso de insulina. Recomenda-se avaliar HbA1c recente (< 3 meses) e garantir controle glicêmico adequado antes do procedimento cirúrgico para reduzir risco de complicações pós-operatórias.",
    confianca: 88,
    referencia: {
      titulo: "Consenso Brasileiro de Catarata e Diabetes - SBO/SBD 2023",
      pagina: "45-48",
      url: "#",
    },
    status: "pendente",
  },
  {
    id: "3",
    tipo: "informacao",
    titulo: "Priorização dentro do tempo de espera aceitável",
    descricao:
      "Tempo de espera atual (8 meses) está dentro do limite estabelecido para casos de prioridade alta com comorbidades. Contudo, o impacto funcional justifica acelerar o agendamento quando houver disponibilidade.",
    confianca: 85,
    referencia: {
      titulo: "Resolução CFM nº 2.149/2016 - Critérios de Priorização",
      pagina: "7-9",
      url: "#",
    },
    status: "pendente",
  },
];

export default function Validation() {
  const handleApprove = () => {
    toast({
      title: "Regulação aprovada",
      description: "A regulação foi aprovada com base nos insights da IA.",
    });
  };

  const handleReject = () => {
    toast({
      title: "Regulação recusada",
      description: "A regulação foi recusada e será retornada para reavaliação.",
      variant: "destructive",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Green Top Bar */}
      <div className="h-3 bg-accent" />
      
      {/* Header */}
      <header className="bg-primary text-primary-foreground py-4 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div>
              <h1 className="text-2xl font-bold uppercase leading-tight">RAR</h1>
              <h1 className="text-xs font-medium uppercase leading-tight tracking-wide">Roteador Adaptativo</h1>
              <h1 className="text-xs font-medium uppercase leading-tight tracking-wide">de Regulação</h1>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium">Prefeitura do</p>
              <p className="text-2xl font-bold">RIO</p>
            </div>
            <div className="border-l border-primary-foreground/30 pl-4">
              <p className="text-lg font-semibold">Saúde</p>
            </div>
            <div className="border-l border-primary-foreground/30 pl-4">
              <p className="text-xl font-bold">SUS+</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Patient Information */}
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-foreground">Ficha de Regulação</h2>
              <Badge variant="info">Caso #2024-10567</Badge>
            </div>
            <PatientCard patient={mockPatient} />
          </div>

          {/* AI Insights */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-bold text-foreground">Insights da Inteligência Artificial</h2>
              <Badge variant="secondary" className="gap-1">
                <Brain className="h-3 w-3" />
                {initialInsights.length} insights
              </Badge>
            </div>
            <div className="space-y-4">
              {initialInsights.map((insight) => (
                <AIInsightCard
                  key={insight.id}
                  insight={insight}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-end gap-4 p-6 bg-card rounded-lg border border-border">
          <Button 
            variant="reject" 
            size="lg"
            onClick={handleReject}
            className="min-w-[180px]"
          >
            Recusar Regulação
          </Button>
          <Button
            variant="approve"
            size="lg"
            onClick={handleApprove}
            className="min-w-[180px]"
          >
            Aprovar Regulação
          </Button>
        </div>
      </main>
    </div>
  );
}
